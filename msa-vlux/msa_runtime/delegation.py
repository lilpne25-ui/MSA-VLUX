"""V4.2+ structured reviewer handoffs; no runtime subagent impersonation."""
from __future__ import annotations
import re,uuid
from .core import load_state,check_chain,atomic_write,jsonbytes,read,safe_payload,now

ROLES={
 'scout':['Identificar fuentes primarias y su fecha','Separar evidencia verificable de inferencia','Reportar UNKNOWN con propietario'],
 'architect':['Evaluar alternativas y dependencias','Analizar integridad, concurrencia y migraciones','Detectar regresiones del diseño'],
 'security':['Buscar rutas de abuso y escalada','Comprobar autorización en servidor y datos sensibles','Exigir controles negativos y aislamiento real'],
 'verifier':['Reproducir afirmaciones clave','Buscar contraejemplos y falsos PASS','Reportar alcance de pruebas no ejecutadas'],
 'experience':['Validar recorridos de usuario con evidencia','Evaluar accesibilidad y rendimiento percibido','Separar simulación de dispositivo real'],
 'operations':['Verificar restauración y rollback','Revisar operación segura y trazas','Distinguir staging y producción'],
 'commercial':['Separar alcance contratado y sugerido','Prohibir porcentajes o ROI inventados','Documentar supuestos y decisiones'],
 'demo':['Separar funcional y simulado','Registrar versión y condiciones de demostración','No prometer funciones no implementadas']
}

def make_packet(project,role,output,master_execution_id):
    if role not in ROLES:raise ValueError('Rol desconocido')
    check_chain(project);state=load_state(project)
    if not state.get('active_atom'):raise ValueError('Se requiere un átomo activo')
    if not re.fullmatch('[A-Za-z0-9_-]{6,100}',master_execution_id):raise ValueError('ID maestro inválido')
    packet={'kind':'msa_review_task','created_at':now(),'role':role,
            'request_id':uuid.uuid4().hex,'project_id':state['project_id'],
            'master_execution_id':master_execution_id,'atom':state['active_atom'],
            'baseline_sha':state['baseline_sha'],
            'checklist':ROLES[role],
            'permissions':{'read_only':True,'external_writes':False,'restricted_data_allowed':False},
            'instructions':'Validar evidencia de fuentes disponibles al reviewer; NO afirmar independencia si no hubo ejecución separada. No ejecutar acciones con efectos externos.',
            'response_contract':['reviewer_execution_id','master_execution_id','role','artifact_sha','findings','result','independence_declared']}
    safe_payload(packet)
    from pathlib import Path
    output=Path(output)
    if output.exists():raise FileExistsError('No se sobrescribe un paquete de revisor')
    atomic_write(output,jsonbytes(packet))
    return packet

def check_review(packet_file,review_file):
    task=read(packet_file);review=read(review_file)
    safe_payload(review)
    for name in ['reviewer_execution_id','master_execution_id','role','artifact_sha','findings','result','independence_declared']:
        if name not in review:raise ValueError('Campo faltante en revisión: '+name)
    if task.get('kind')!='msa_review_task' or review['role']!=task['role'] or review['master_execution_id']!=task['master_execution_id']:
        raise ValueError('Revisión no corresponde al paquete')
    if not review['artifact_sha'] or review['artifact_sha']!=task['baseline_sha']:
        raise ValueError('SHA revisado diferente del baseline')
    if review['reviewer_execution_id']==task['master_execution_id']:
        raise ValueError('Un proceso no puede autoacreditarse independiente')
    if not isinstance(review['findings'],list):raise ValueError('Hallazgos no son una lista')
    if review['result'] not in ['PASS_WITH_RESERVATIONS','BLOCKED','PASS_REPORTED']:
        raise ValueError('Resultado inválido')
    if review['independence_declared'] is not True:
        return {'status':'NOT_INDEPENDENT','findings':len(review['findings']),'reviewer_role':review['role']}
    return {'status':'DECLARED_INDEPENDENT_NOT_ATTESTED','findings':len(review['findings']),
            'reviewer_role':review['role'],'artifact_sha':review['artifact_sha'],
            'blocking_findings':sum(x.get('severity') in ('CRITICAL','HIGH') for x in review['findings']),
            'caveat':'Distinct IDs are not external proof of process/permission separation'}
