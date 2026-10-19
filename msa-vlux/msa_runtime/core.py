"""Portable, conservative MSA ledger. Standard library only. Not a security boundary."""
from __future__ import annotations
import hashlib, json, os, re, tempfile, time, uuid
from datetime import datetime, timezone
from pathlib import Path

FORMAT = 1
TYPES = {'evidence','decision','risk','run','approval','action','review','metric','checkpoint'}
SENSITIVE_KEY = re.compile(r'(password|passwd|secret|api[_-]?key|access[_-]?token|refresh[_-]?token|private[_-]?key|credential|cookie|authorization)', re.I)
SENSITIVE_VALUE = re.compile(r'(-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_|github_pat_|sk-[A-Za-z0-9]{12})[A-Za-z0-9_\-]{8,}|Bearer\s+\S+)', re.I)


def now(): return datetime.now(timezone.utc).isoformat(timespec='seconds')
def jsonbytes(obj): return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',',':')).encode('utf-8')
def digest(data): return hashlib.sha256(data).hexdigest()
def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def atomic_write(path, data):
    p=Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='wb',prefix='.msa-',dir=p.parent,delete=False) as f:
        tmp=Path(f.name); f.write(data); f.flush(); os.fsync(f.fileno())
    try: os.replace(tmp,p)
    finally: tmp.unlink(missing_ok=True)

def safe_payload(data):
    raw=jsonbytes(data)
    if len(raw)>32768: raise ValueError('Payload excesivo: use referencias y hashes, no contenido en bruto')
    def check(value):
        if isinstance(value,dict):
            for key,item in value.items():
                if SENSITIVE_KEY.search(str(key)): raise ValueError('Campo sensible rechazado: '+str(key))
                check(item)
        elif isinstance(value,list):
            for item in value: check(item)
        elif isinstance(value,str) and SENSITIVE_VALUE.search(value):
            raise ValueError('Valor posiblemente secreto rechazado')
    check(data)
    return data

def root(project): return Path(project).expanduser().resolve()/'.msa'
def state_path(project): return root(project)/'state.json'
def load_state(project):
    p=state_path(project)
    if not p.exists():raise ValueError('Sin expediente .msa: ejecute init o import-handoff')
    state=read(p)
    if state.get('format')!=FORMAT:raise ValueError('Formato de expediente no soportado')
    return state

def init(project, name, version):
    folder=root(project)
    if folder.exists():raise FileExistsError('Ya existe un expediente; no se sobrescribe')
    folder.mkdir(parents=True)
    state={'format':FORMAT,'msa_version':version,'project_id':uuid.uuid4().hex,'project_label':name,
           'created_at':now(),'lifecycle':'UNASSIGNED','active_atom':None,'baseline_sha':None,
           'approval_transferable':False,'last_event_hash':'0'*64,'last_event_count':0,
           'external_write_authorized':False}
    safe_payload(state)
    atomic_write(folder/'state.json',jsonbytes(state))
    (folder/'history.jsonl').write_text('',encoding='utf-8')
    return state

def events(project):
    p=root(project)/'history.jsonl'
    return [json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()] if p.exists() else []

def check_chain(project):
    state=load_state(project); prior='0'*64; records=events(project)
    for n,event in enumerate(records,1):
        if event.get('seq')!=n or event.get('prev_hash')!=prior:raise ValueError('Cadena de evidencia alterada: seq '+str(n))
        candidate={k:v for k,v in event.items() if k!='hash'}
        if digest(jsonbytes(candidate))!=event.get('hash'):raise ValueError('Hash incorrecto: seq '+str(n))
        prior=event['hash']
    if state['last_event_hash']!=prior or state['last_event_count']!=len(records):raise ValueError('Estado e historial inconsistentes')
    return {'events':len(records),'last_hash':prior,'project_id':state['project_id']}

class Mutex:
    def __init__(self,p):self.p=p
    def __enter__(self):
        for _ in range(40):
            try:
                self.fd=os.open(self.p,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                os.write(self.fd,str(os.getpid()).encode());return self
            except FileExistsError:time.sleep(.1)
        raise TimeoutError('Expediente ocupado: no se elimina bloqueo automáticamente')
    def __exit__(self,*args):os.close(self.fd);self.p.unlink(missing_ok=True)

def append(project,kind,payload,actor='agent'):
    if kind not in TYPES:raise ValueError('Tipo de evento no permitido')
    safe_payload(payload)
    folder=root(project)
    with Mutex(folder/'.write.lock'):
        prior=check_chain(project);state=load_state(project)
        if kind=='metric' and isinstance(payload,dict) and payload.get('execution_id'):
            if any(e['type']=='metric' and e['payload'].get('execution_id')==payload['execution_id'] for e in events(project)):
                raise ValueError('execution_id duplicado en el expediente')
        event={'seq':prior['events']+1,'id':uuid.uuid4().hex,'time':now(),'type':kind,
               'actor':actor,'payload':payload,'prev_hash':prior['last_hash']}
        event['hash']=digest(jsonbytes(event))
        with (folder/'history.jsonl').open('ab') as f:
            f.write(jsonbytes(event)+b'\n');f.flush();os.fsync(f.fileno())
        state.update(last_event_hash=event['hash'],last_event_count=event['seq'])
        atomic_write(folder/'state.json',jsonbytes(state))
    return event

def set_atom(project,atom,mode,status,baseline=None):
    if not re.fullmatch(r'[A-Za-z0-9][\w.\-]{0,48}',atom):raise ValueError('ID de átomo inválido')
    if mode not in {'DISCOVERY','AUDIT','DELIVERY','OPERATIONS','EVOLUTION','PRODUCTION'}:raise ValueError('Modo inválido')
    if status not in {'planned','in_progress','blocked','completed_with_reservations','completed'}:raise ValueError('Estado inválido')
    payload={'atom':atom,'mode':mode,'status':status,'baseline_sha':baseline}
    with Mutex(root(project)/'.write.lock'):
        prior=check_chain(project);state=load_state(project)
        event={'seq':prior['events']+1,'id':uuid.uuid4().hex,'time':now(),'type':'checkpoint',
               'actor':'msa-cli','payload':payload,'prev_hash':prior['last_hash']}
        event['hash']=digest(jsonbytes(event))
        with (root(project)/'history.jsonl').open('ab') as f:
            f.write(jsonbytes(event)+b'\n');f.flush();os.fsync(f.fileno())
        state.update(active_atom={'id':atom,'mode':mode,'status':status,'updated_at':now()},lifecycle=mode,
                     last_event_hash=event['hash'],last_event_count=event['seq'])
        if baseline:state['baseline_sha']=baseline
        atomic_write(state_path(project),jsonbytes(state))
    return state['active_atom']

def doctor(package_root,version):
    r=Path(package_root)
    modules=sorted(x.stem for x in (r/'modules').glob('*.md'))
    return {'msa_version':version,'python':'stdlib','modules':modules,'module_count':len(modules),
            'technical_guards':'not_verified','external_write_authorized':False,
            'codex_runtime':'instructions_only_until_installed','claude_runtime':'instructions_only_until_installed',
            'roles':'declared_not_independent_until_executed'}


def verify_package(package_root):
    package_root=Path(package_root).resolve()
    manifest=package_root/'SHA256SUMS.txt'
    if not manifest.is_file():raise ValueError('Falta el manifiesto SHA256SUMS.txt')
    hashes={}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        sha,sep,rel=line.partition('  ')
        if not sep or not re.fullmatch('[0-9a-f]{64}',sha) or not rel or rel in hashes:
            raise ValueError('Formato de manifiesto inválido')
        hashes[rel]=sha
    files={p.relative_to(package_root).as_posix() for p in package_root.rglob('*') if p.is_file()
           and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='SHA256SUMS.txt'}
    if files!=set(hashes):raise ValueError('Archivos faltantes o agregados respecto al manifiesto')
    for rel,sha in hashes.items():
        path=package_root/rel
        if path.is_symlink() or not path.resolve().is_relative_to(package_root):
            raise ValueError('Enlace no permitido en la skill')
        if digest(path.read_bytes())!=sha:raise ValueError('Hash inválido en '+rel)
    return {'verified':True,'files':len(hashes),'note':'Integrity against local manifest; not provenance or signature'}
