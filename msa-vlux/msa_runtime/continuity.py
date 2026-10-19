"""Explicit, bounded handoffs between environments; no secret or approval transfer."""
from __future__ import annotations
import hashlib,json,os,re,shutil,tempfile,zipfile
from pathlib import Path
from .core import load_state,check_chain,root,safe_payload,jsonbytes,digest,now,atomic_write

FILES=['state.json','history.jsonl']
MAX_FILE=3*1024*1024
ALLOWED_EXT={'.md','.txt','.json','.csv','.log','.yaml','.yml'}
BLOCKED_NAMES={'.env','.git','node_modules','secrets','private','credentials','id_rsa'}

def build_handoff(project,output,runtime,includes=()):
    if runtime not in ('codex','claude-code','claude-cloud','other'):raise ValueError('Runtime no soportado')
    check_chain(project); folder=root(project);state=load_state(project)
    blob={}
    for filename in FILES:
        p=folder/filename
        if p.is_symlink() or not p.is_file():raise ValueError('Archivo inválido')
        raw=p.read_bytes()
        if len(raw)>MAX_FILE:raise ValueError('Handoff excede límite de archivo')
        blob['state/'+filename]=raw
    # Sanitize portable state: explicit write approvals never travel.
    snapshot=json.loads(blob['state/state.json'])
    snapshot['external_write_authorized']=False
    snapshot['approval_transferable']=False
    snapshot['last_handoff_at']=now()
    snapshot['source_runtime']=runtime
    safe_payload(snapshot)
    blob['state/state.json']=jsonbytes(snapshot)
    manifest={'format':1,'kind':'msa-portable-handoff','source_runtime':runtime,
              'origin_version':state['msa_version'],'project_id':state['project_id'],
              'created_at':now(),'requires_reauthorization':True,
              'files':{name:{'sha256':digest(raw),'size':len(raw)} for name,raw in sorted(blob.items())}}
    project_path=Path(project).expanduser().resolve()
    if len(includes)>20:raise ValueError('Máximo 20 evidencias explícitas')
    for candidate in includes:
        rawpath=Path(candidate)
        path=(rawpath if rawpath.is_absolute() else project_path/rawpath)
        if path.is_symlink():raise ValueError('No se aceptan symlinks')
        path=path.resolve()
        if not path.is_relative_to(project_path):raise ValueError('Evidencia fuera del proyecto')
        rel=path.relative_to(project_path)
        if any(part.lower() in BLOCKED_NAMES or part.startswith('.') for part in rel.parts):
            raise ValueError('Ruta privada o oculta rechazada: '+str(rel))
        if path.suffix.lower() not in ALLOWED_EXT:raise ValueError('Extensión no permitida: '+str(rel))
        if not path.is_file() or path.stat().st_size>MAX_FILE:raise ValueError('Archivo ausente o demasiado grande')
        raw=path.read_bytes()
        try:text=raw.decode('utf-8')
        except UnicodeError:raise ValueError('Evidencia no UTF-8')
        safe_payload({'text':text})  # Rechazo conservador; NO sustituye revisión humana de privacidad.
        key='evidence/'+rel.as_posix()
        if key in blob:raise ValueError('Archivo duplicado')
        blob[key]=raw
        manifest['files'][key]={'sha256':digest(raw),'size':len(raw)}
    blob['MANIFEST.json']=jsonbytes(manifest)
    text=(f"MSA-VLUX HANDOFF\nProyecto: {state['project_label']}\n"
          f"ID: {state['project_id']}\nAtomo: {state.get('active_atom')}\n"
          f"SHA base: {state.get('baseline_sha')}\n"
          'Verifique el ZIP con verify-handoff, importe con import-handoff y ejecute status. '
          'Las autorizaciones externas NO se transfieren. El código, los archivos de proyecto y los adjuntos no se incluyen; '
          'reconéctelos mediante fuentes verificadas. Guarde el ZIP en almacenamiento privado.\n')
    blob['LEEME-REANUDAR.txt']=text.encode()
    out=Path(output).expanduser().resolve();out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise FileExistsError('Destino ya existe; no sobrescribir')
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for filename,raw in sorted(blob.items()):z.writestr(filename,raw)
    return {'zip':str(out),'sha256':digest(out.read_bytes()),'project_id':state['project_id'],'size':out.stat().st_size}

def verify_handoff(archive):
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist()
        if len(infos)>24:raise ValueError('Entradas extra inesperadas')
        names={a.filename for a in infos}
        if len(names)!=len(infos):raise ValueError('Nombres ZIP duplicados')
        required={'state/state.json','state/history.jsonl','MANIFEST.json','LEEME-REANUDAR.txt'}
        if not required.issubset(names):raise ValueError('Faltan archivos esenciales')
        for name in names-required:
            p=Path(name)
            if not name.startswith('evidence/') or p.is_absolute() or '..' in p.parts or any(k.lower() in BLOCKED_NAMES or k.startswith('.') for k in p.parts) or p.suffix.lower() not in ALLOWED_EXT:
                raise ValueError('Ruta de evidencia no permitida')
        for i in infos:
            if i.is_dir() or i.file_size>MAX_FILE or (i.external_attr>>16)&0o170000==0o120000:
                raise ValueError('Entrada inválida / symlink / excesiva')
        m=json.loads(z.read('MANIFEST.json'))
        if m.get('kind')!='msa-portable-handoff' or m.get('format')!=1:raise ValueError('Manifiesto inválido')
        if set(m['files'])!=names-{'MANIFEST.json','LEEME-REANUDAR.txt'}:
            raise ValueError('Manifiesto no cubre todas las entradas')
        for filename in sorted(m['files']):
            raw=z.read(filename)
            if digest(raw)!=m['files'][filename]['sha256'] or len(raw)!=m['files'][filename]['size']:
                raise ValueError('Integridad incorrecta: '+filename)
        s=json.loads(z.read('state/state.json'))
        if s.get('project_id')!=m.get('project_id') or s.get('external_write_authorized') or s.get('approval_transferable'):
            raise ValueError('Identidad o autorización no válidas')
        hist=[json.loads(line) for line in z.read('state/history.jsonl').decode().splitlines() if line.strip()]
        prev='0'*64
        for n,e in enumerate(hist,1):
            if e['seq']!=n or e['prev_hash']!=prev or e['hash']!=digest(jsonbytes({k:v for k,v in e.items() if k!='hash'})):
                raise ValueError('Cadena interna alterada')
            prev=e['hash']
        if prev!=s['last_event_hash'] or len(hist)!=s['last_event_count']:raise ValueError('Estado inconsistente')
        return {'verified':True,'project_id':s['project_id'],'events':len(hist),'baseline_sha':s.get('baseline_sha'),
                'approval_transferable':False,'msa_version':s['msa_version']}

def import_handoff(archive,target):
    info=verify_handoff(archive)
    project=Path(target).expanduser().resolve();folder=project/'.msa'
    if folder.exists():raise FileExistsError('No se sobrescribe un expediente existente')
    project.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix='.msa-import-',dir=project))
    try:
        with zipfile.ZipFile(archive) as z:
            for f in FILES:(tmp/f).write_bytes(z.read('state/'+f))
            for n in z.namelist():
                if n.startswith('evidence/'):
                    p=tmp/'imported-evidence'/n[len('evidence/'):]
                    p.parent.mkdir(parents=True,exist_ok=True)
                    p.write_bytes(z.read(n))
        # Always reset authorization and record environment provenance only in state.
        state=json.loads((tmp/'state.json').read_text())
        state['external_write_authorized']=False;state['approval_transferable']=False
        state['resumed_at']=now();state['resumed_from_sha256']=digest(Path(archive).read_bytes())
        atomic_write(tmp/'state.json',jsonbytes(state))
        tmp.rename(folder)
        check_chain(project)
        return info
    finally:
        if tmp.exists():shutil.rmtree(tmp)

def resume_report(project):
    chk=check_chain(project); s=load_state(project)
    return {'msa_version':s['msa_version'],'project_id':s['project_id'],
            'project_label':s['project_label'],'active_atom':s['active_atom'],
            'baseline_sha':s['baseline_sha'],'events':chk['events'],
            'required':'Verify repository SHA and source files, rebuild missing external evidence, re-establish permission scope',
            'external_write_authorized':False,'independent_review':'not_verified_until_rechecked',
            'imported_evidence_files':len(list((root(project)/'imported-evidence').rglob('*'))) if (root(project)/'imported-evidence').exists() else 0}
