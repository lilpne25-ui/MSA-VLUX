"""Local privacy-minimal observations. Records claims, not attested measurements.

No network, shell, repository or external service integration. A runner can export
structured local JSON, but external provenance MUST be independently verified.
"""
from __future__ import annotations
import math, statistics
from . import core

RUNTIMES = {'codex','claude-code','claude-cloud','human','other'}
PROVENANCE = {'synthetic','manual','instrumented-unverified','instrumented-attested'}


def _natural(x, name):
    if type(x) is not int or x < 0 or x > 10_000_000: raise ValueError(f'{name}: entero no negativo requerido')
    return x


def validate(row):
    if not isinstance(row, dict): raise ValueError('Observacion debe ser objeto')
    fields = {'execution_id','task_id','suite_id','strategy','runtime','provenance','artifact_sha256',
              'tests_passed','tests_total','evidence_verified','evidence_total',
              'handoffs_restored','handoffs_attempted','policy_violations','critical_regressions',
              'duration_seconds','cost_usd'}
    if set(row) != fields: raise ValueError('Campos desconocidos o faltantes; usar contrato de observacion exacto')
    for name in ('execution_id','task_id','suite_id','strategy'):
        value=row[name]
        if not isinstance(value,str) or not 1<=len(value)<=80 or not all(c.isalnum() or c in '_-.' for c in value):
            raise ValueError(f'{name} identificador inválido')
    if row['runtime'] not in RUNTIMES or row['provenance'] not in PROVENANCE:raise ValueError('Runtime/provenance inválido')
    if not isinstance(row['artifact_sha256'],str) or len(row['artifact_sha256'])!=64 or any(c not in '0123456789abcdef' for c in row['artifact_sha256']):
        raise ValueError('artifact_sha256 inválido')
    for k in ('tests_passed','tests_total','evidence_verified','evidence_total','handoffs_restored','handoffs_attempted','policy_violations','critical_regressions'):_natural(row[k],k)
    for a,b in [('tests_passed','tests_total'),('evidence_verified','evidence_total'),('handoffs_restored','handoffs_attempted')]:
        if row[a]>row[b]:raise ValueError(f'{a} excede {b}')
    for k in ('duration_seconds','cost_usd'):
        v=row[k]
        if v is None and k=='cost_usd':continue
        if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=10**8:
            raise ValueError(f'{k}: número inválido')
    if row['provenance']=='instrumented-attested':
        # A JSON assertion is not attestation. Only a signed external provenance
        # verifier could upgrade the claim; not implemented here.
        raise ValueError('La procedencia attestada no puede declararse por JSON externo')
    core.safe_payload(row)
    return row


def ingest(project, record):
    validate(record)
    existing = [e['payload']['execution_id'] for e in core.events(project) if e['type']=='metric' and 'execution_id' in e['payload']]
    if record['execution_id'] in existing:raise ValueError('execution_id duplicado en el expediente')
    return core.append(project,'metric',record,actor='metrics-importer')


def summary(project):
    core.check_chain(project)
    metrics=[e['payload'] for e in core.events(project) if e['type']=='metric' and 'execution_id' in e['payload']]
    groups={}
    for row in metrics:groups.setdefault(row['strategy'],[]).append(row)
    out={}
    for name, rows in sorted(groups.items()):
        def ratio(a,b):
            numer=sum(x[a] for x in rows);denom=sum(x[b] for x in rows)
            return round(numer/denom,6) if denom else None
        out[name]={
          'executions':len(rows), 'test_pass_rate':ratio('tests_passed','tests_total'),
          'evidence_coverage':ratio('evidence_verified','evidence_total'),
          'handoff_recovery_rate':ratio('handoffs_restored','handoffs_attempted'),
          'duration_median_seconds':round(statistics.median(x['duration_seconds'] for x in rows),3),
          'cost_sum_usd':round(sum(x['cost_usd'] for x in rows if x['cost_usd'] is not None),4) if all(x['cost_usd'] is not None for x in rows) else None,
          'policy_violations':sum(x['policy_violations'] for x in rows),
          'critical_regressions':sum(x['critical_regressions'] for x in rows),
          'provenance_counts':{p:sum(x['provenance']==p for x in rows) for p in sorted(PROVENANCE) if any(x['provenance']==p for x in rows)},
          'caveat':'Mediciones declaradas/importadas; no equivalen a auditoría independiente'}
    return {'kind':'msa_observations_summary','project_id':core.load_state(project)['project_id'],'records':len(metrics),'by_strategy':out,
            'privacy':'no raw prompts, outputs, credentials, emails or personal performance scores'}


def calibration(project):
    core.check_chain(project)
    pairs={}
    for e in core.events(project):
        if e['type']!='review':continue
        data=e['payload']
        if data.get('kind')!='calibration':continue
        if set(data)!={'kind','task_id','role','score','instrumented_evidence'}:continue
        if data['role'] not in ('self','verifier') or type(data['score']) is not int or not 0<=data['score']<=4:continue
        pairs.setdefault(data['task_id'],{})[data['role']]=data
    matched=[a for a in pairs.values() if 'self' in a and 'verifier' in a]
    return {'pairs':len(matched),'mean_absolute_error':round(sum(abs(p['self']['score']-p['verifier']['score']) for p in matched)/len(matched),4) if matched else None,
            'average_self_overstatement':round(sum(p['self']['score']-p['verifier']['score'] for p in matched)/len(matched),4) if matched else None,
            'independent_reviews_attested':0,'caveat':'La identidad del revisor NO puede verificarse a partir del expediente local'}
