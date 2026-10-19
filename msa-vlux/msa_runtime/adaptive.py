"""V6 bounded strategy selection, with conservative risk gates and no execution."""
from __future__ import annotations
from .core import now

MODES={'AUDIT','DISCOVERY','DELIVERY','EVOLUTION','OPERATIONS','PRODUCTION'}
RISK={'low','medium','high','unknown'}

def plan(request, experiment=None):
    keys={'task_id','mode','risk','complexity','data_class','needs_external_write'}
    if not isinstance(request,dict) or set(request)!=keys:raise ValueError('Perfil requiere contrato exacto')
    if request['mode'] not in MODES or request['risk'] not in RISK or request['complexity'] not in ('small','medium','large'):
        raise ValueError('Modo/riesgo/complejidad inválidos')
    if request['data_class'] not in ('synthetic','internal','restricted','unknown') or type(request['needs_external_write']) is not bool:
        raise ValueError('Clase de datos/efecto inválido')
    if not isinstance(request['task_id'],str) or not request['task_id'] or len(request['task_id'])>80 or not all(x.isalnum() or x in '_-.' for x in request['task_id']):
        raise ValueError('ID inválido')
    elevated=(request['risk'] in ('high','unknown') or request['data_class'] in ('restricted','unknown') or request['mode']=='PRODUCTION')
    thorough=elevated or request['complexity']=='large' or request['risk']=='medium'
    strategy='FULL_ADVERSARIAL' if elevated else 'FULL' if thorough else 'LITE'
    gates=['baseline_identified','permission_scope_declared','evidence_saved','self_assessment','checkpoints_recoverable']
    if thorough:gates+=['reproducible_tests','negative_tests','independent_review_requested']
    if elevated:gates+=['threat_model','isolation_verified','restore_or_rollback_test','independent_review_required']
    if request['needs_external_write']:gates+=['explicit_external_authorization','runtime_access_enforced']
    proposal = None
    if experiment is not None:
        if not isinstance(experiment,dict) or experiment.get('kind')!='paired_proposal':raise ValueError('Evidencia experimental inválida')
        proposal = {'experiment_id':experiment.get('experiment_id'),
                    'recommendation':'CANDIDATE_FOR_HUMAN_REVIEW' if experiment.get('decision')=='PROPOSE_FOR_HUMAN_REVIEW' and experiment.get('auto_apply') is False else 'REJECT',
                    'experimental_data_attested':False,
                    'changes_applied':False}
    return {'kind':'msa_adaptive_plan','task_id':request['task_id'],'created_at':now(),'strategy':strategy,
            'required_gates':sorted(set(gates)),'allowed_external_writes':False,
            'run_approved':False,'promotion_allowed':False,'experiment_proposal':proposal,
            'model_chosen_strategy_not_human_approval':True,
            'notes':'Sugerencia por reglas conservadoras. No ejecuta código ni cambia política; revisar con responsable humano.'}
