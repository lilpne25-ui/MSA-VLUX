"""Falsifiable, deterministic trace checks and evidence-linked self-evaluation."""
from __future__ import annotations
from pathlib import Path
import re
from .core import read,events,safe_payload,now,jsonbytes,atomic_write

DIMENSIONS=['accuracy','evidence','permissions','security','recovery','delivery']

def evaluate(scenarios,traces):
    sc=read(scenarios)['scenarios']; observed=read(traces)['traces']
    outcome=[]
    for item in sc:
        seen=observed.get(item['id'],[])
        if not isinstance(seen,list):raise ValueError('Traza no es una lista')
        needs=item.get('required_events',[]);bans=item.get('forbidden_events',[])
        missing=[x for x in needs if x not in seen]
        forbidden=[x for x in bans if x in seen]
        order=item.get('ordered_events',[])
        bad_order=False;pos=0
        for target in order:
            try:pos=seen.index(target,pos)+1
            except ValueError:bad_order=True;break
        ok=not(missing or forbidden or bad_order)
        outcome.append({'id':item['id'],'pass':ok,'missing':missing,'forbidden_seen':forbidden,'wrong_order':bad_order,
                        'observations_count':len(seen)})
    return {'kind':'deterministic_trace_evaluation','source':'supplied_trace_not_host_attested',
            'scenarios':len(outcome),'passed':sum(x['pass'] for x in outcome),
            'failed':sum(not x['pass'] for x in outcome),'details':outcome}

def self_assess(project,input_file):
    payload=read(input_file)
    safe_payload(payload)
    evidence={x['id']:x['payload'] for x in events(project) if x['type']=='evidence'}
    items=payload.get('dimensions',{})
    if sorted(items)!=sorted(DIMENSIONS):raise ValueError('Faltan dimensiones del examen')
    detail={};total=0
    for dim in DIMENSIONS:
        x=items[dim];score=x['score'];refs=x.get('evidence_ids',[])
        if not isinstance(score,int) or not 0<=score<=4:raise ValueError('Puntuación 0..4 requerida')
        if score>2 and not refs:raise ValueError('Puntuación alta sin evidencia: '+dim)
        if any(k not in evidence for k in refs):raise ValueError('Evidencia inexistente: '+dim)
        if score>2 and not any(re.fullmatch(r'[0-9a-fA-F]{64}',str(evidence[k].get('artifact_sha256',''))) and evidence[k].get('result')=='PASS' for k in refs):
            raise ValueError('Para puntuación alta se exige evidencia PASS con SHA-256: '+dim)
        detail[dim]={'score':score,'evidence_ids':refs,'claim':x.get('claim','')}
        total+=score
    return {'kind':'self_assessment','time':now(),'source':'self_report_not_independent',
            'score':total,'max_score':24,'dimensions':detail,'human_review':'not_verified',
            'independent_review':'not_verified'}
