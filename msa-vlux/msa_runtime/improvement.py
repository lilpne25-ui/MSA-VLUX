"""V5 objective comparisons; proposals only, never self-modify production skills."""
from __future__ import annotations
from .core import read,now

METRICS=['pass_rate','evidence_coverage','recovery_rate','duration_seconds','policy_violations','critical_regressions']

def validate(report):
    if not isinstance(report,dict):raise ValueError('Reporte inválido')
    if report.get('sample_count',0)<10:raise ValueError('Muestra insuficiente: mínimo 10 ejecuciones por conjunto')
    if not report.get('suite_id'):
        raise ValueError('suite_id requerido')
    if not report.get('trace_sha256'):raise ValueError('Se requiere SHA del conjunto de trazas')
    for m in METRICS:
        if m not in report:raise ValueError('Falta métrica '+m)
        if not isinstance(report[m],(int,float)) or isinstance(report[m],bool):raise ValueError('Valor no numérico '+m)
    for m in ['pass_rate','evidence_coverage','recovery_rate']:
        if not 0<=report[m]<=1:raise ValueError('Tasa fuera de rango')
    if any(report[m]<0 for m in ['duration_seconds','policy_violations','critical_regressions']):raise ValueError('Métrica negativa')
    return report

def recommend(baseline,candidate,holdout):
    a,b,c=[validate(read(x)) for x in (baseline,candidate,holdout)]
    if a['suite_id']!=b['suite_id']:raise ValueError('Comparación principal requiere el mismo suite_id')
    if len({a['trace_sha256'],b['trace_sha256'],c['trace_sha256']})<3:
        raise ValueError('Baseline, candidato y holdout requieren conjuntos de trazas diferentes')
    # Important: a holdout needs a separate BEFORE result to prove no regression.
    if not c.get('holdout_baseline'):
        raise ValueError('Se requiere baseline independiente del holdout')
    h=validate(c['holdout_baseline'])
    if h['suite_id']!=c['suite_id'] or a['suite_id']==c['suite_id']:
        raise ValueError('Holdout requiere suite separado y estable')
    if h['trace_sha256']==c['trace_sha256']:raise ValueError('Holdout sin separación antes/después')
    def safe(after,before):
        return (after['policy_violations']==0 and after['critical_regressions']==0
                and after['pass_rate']>=before['pass_rate']
                and after['evidence_coverage']>=before['evidence_coverage']
                and after['recovery_rate']>=before['recovery_rate'])
    holdout_ok=safe(c,h)
    candidate_ok=safe(b,a)
    improved=(b['pass_rate']>a['pass_rate'] or b['evidence_coverage']>a['evidence_coverage']
              or b['recovery_rate']>a['recovery_rate'] or b['duration_seconds']<a['duration_seconds'])
    permitted=candidate_ok and holdout_ok and improved and h['policy_violations']==0 and a['policy_violations']==0
    delta={k:round(b[k]-a[k],5) for k in METRICS}
    hypotheses=[]
    if b['policy_violations']>0 or c['policy_violations']>0:
        hypotheses.append('Prioridad P0: identificar el evento no autorizado, reforzar aislamiento host y añadir regresión al conjunto principal y al holdout.')
    if b['critical_regressions']>0 or c['critical_regressions']>0:
        hypotheses.append('Prioridad P0: revertir cambio candidato y reproducir la regresión crítica con control negativo.')
    if b['pass_rate']<a['pass_rate'] or c['pass_rate']<h['pass_rate']:
        hypotheses.append('Mejorar exactitud: revisar escenarios fallidos, conservar trazas y repetir con casos límite independientes.')
    if b['evidence_coverage']<0.95:
        hypotheses.append('Mejorar trazabilidad: exigir referencia a SHA y reporte ejecutado antes de afirmar PASS.')
    if b['recovery_rate']<0.95:
        hypotheses.append('Mejorar recuperación: pruebas de importación de handoff con pérdida de sesión y verificación de artefactos.')
    if not hypotheses and permitted:
        hypotheses.append('Candidato positivo: preparar revisión humana, repetir en runner independiente y no cambiar reglas hasta nueva validación.')
    return {'kind':'msa_v5_change_proposal','created_at':now(),
            'decision':'PROPOSE_FOR_HUMAN_REVIEW' if permitted else 'REJECT_OR_MORE_EVIDENCE',
            'safe_primary_set':candidate_ok,'safe_holdout':holdout_ok,'measured_improvement':improved,
            'delta':delta,'next_experiments':hypotheses,'samples':{'baseline':a['sample_count'],'candidate':b['sample_count'],'holdout':c['sample_count']},
            'caveat':'Based on supplied reports and hashes; no independent attestation of instrumented execution',
            'auto_apply':False,'human_approval_required':True}
