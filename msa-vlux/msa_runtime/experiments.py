"""Offline deterministic optimizers and conservative paired experiment analysis.

These benchmark optimizers optimize SYNTHETIC functions; they do not tune agent
instructions or affect deployed systems. No arbitrary eval/exec or remote calls.
"""
from __future__ import annotations
import math,random,statistics
from .core import read, now

FUNCTIONS={'sphere':lambda xs:sum(x*x for x in xs),
           'rastrigin':lambda xs:10*len(xs)+sum(x*x-10*math.cos(2*math.pi*x) for x in xs)}


def optimize(config):
    if not isinstance(config,dict) or set(config)!={'function','dimensions','lower','upper','budget','seed','algorithm'}:
        raise ValueError('Config exige exactamente function/dimensions/lower/upper/budget/seed/algorithm')
    fn=config['function'];alg=config['algorithm'];d=config['dimensions'];n=config['budget'];seed=config['seed']
    if fn not in FUNCTIONS or alg not in ('random','pso'):raise ValueError('Solo funciones sintéticas y algoritmos permitidos')
    if type(d)!=int or not 1<=d<=12 or type(n)!=int or not 20<=n<=2000 or type(seed)!=int or not 0<=seed<2**32:raise ValueError('Parámetros fuera de límites')
    low,high=config['lower'],config['upper']
    if any(isinstance(v,bool) or not isinstance(v,(float,int)) or not math.isfinite(v) for v in [low,high]) or not -50<=low<high<=50:
        raise ValueError('Rango inválido')
    rng=random.Random(seed);objective=FUNCTIONS[fn];best_value=float('inf');best=None;history=[]
    def score(point):
        nonlocal best,best_value
        value=objective(point)
        if value<best_value:best_value=value;best=list(point)
        history.append(round(best_value,8))
    if alg=='random':
        for _ in range(n):score([rng.uniform(low,high) for _ in range(d)])
    else:
        swarm=min(16,max(4,n//12))
        positions=[[rng.uniform(low,high) for _ in range(d)] for _ in range(swarm)]
        velocities=[[0.0]*d for _ in range(swarm)]
        personal=[list(pos) for pos in positions]
        personal_v=[float('inf')]*swarm
        for step in range(n):
            i=step%swarm
            if step>=swarm:
                for j in range(d):
                    velocities[i][j]=0.6*velocities[i][j]+1.35*rng.random()*(personal[i][j]-positions[i][j])+1.35*rng.random()*(best[j]-positions[i][j])
                    velocities[i][j]=max(-(high-low),min(high-low,velocities[i][j]))
                    positions[i][j]=max(low,min(high,positions[i][j]+velocities[i][j]))
            pos=positions[i]
            val=objective(pos)
            if val<personal_v[i]:personal_v[i]=val;personal[i]=list(pos)
            score(pos)
    return {'kind':'synthetic_benchmark','algorithm':alg,'function':fn,'seed':seed,'evaluations':n,
            'best_value':round(best_value,8),'best_position':[round(x,8) for x in best],
            'history':history,'scope':'synthetic_only','external_effects':False}


def paired_analysis(data):
    """Prospective paired comparison, split by explicit train/holdout; only proposes.
    An observation contains task ID, split, baseline/candidate test pass, duration,
    violations, and source. This is an analysis of supplied numbers, not attestation.
    """
    if not isinstance(data,dict) or set(data)!={'experiment_id','observations'}:raise ValueError('Formato de experimento inválido')
    if not isinstance(data['experiment_id'],str) or not 1<=len(data['experiment_id'])<=80 or not all(c.isalnum() or c in '_-.' for c in data['experiment_id']):raise ValueError('ID requerido')
    obs=data['observations'];
    if not isinstance(obs,list) or not 10<=len(obs)<=2000:raise ValueError('10-2000 tareas pareadas requeridas')
    splits={'train':[],'holdout':[]};seen=set()
    keys={'task_id','split','baseline_pass','candidate_pass','baseline_duration','candidate_duration','baseline_violations','candidate_violations','baseline_critical','candidate_critical'}
    for x in obs:
        if not isinstance(x,dict) or set(x)!=keys:raise ValueError('Observación inválida')
        if x['split'] not in splits or not isinstance(x['task_id'],str) or not 1<=len(x['task_id'])<=80 or not all(c.isalnum() or c in '_-.' for c in x['task_id']) or x['task_id'] in seen:raise ValueError('Split/ID inválido o duplicado')
        seen.add(x['task_id'])
        for key in ('baseline_pass','candidate_pass'):
            if type(x[key]) is not bool:raise ValueError('Pass requiere bool')
        for key in ('baseline_violations','candidate_violations','baseline_critical','candidate_critical'):
            if type(x[key]) is not int or x[key]<0:raise ValueError('Contador inválido')
        for key in ('baseline_duration','candidate_duration'):
            if type(x[key]) not in (int,float) or not math.isfinite(x[key]) or x[key]<0:raise ValueError('Tiempo inválido')
        splits[x['split']].append(x)
    if len(splits['train'])<5 or len(splits['holdout'])<5:raise ValueError('Train y holdout requieren >=5 casos')
    def stats(rows):
        n=len(rows);b=sum(x['baseline_pass'] for x in rows)/n;c=sum(x['candidate_pass'] for x in rows)/n
        violations=sum(x['candidate_violations'] for x in rows);critical=sum(x['candidate_critical'] for x in rows)
        mean_delta=statistics.mean(x['candidate_duration']-x['baseline_duration'] for x in rows)
        return {'n':n,'baseline_pass_rate':round(b,4),'candidate_pass_rate':round(c,4),
                'delta_pass_rate':round(c-b,4),'mean_duration_delta_seconds':round(mean_delta,4),
                'candidate_policy_violations':violations,'candidate_critical_regressions':critical,
                'regressed_tasks':sum(x['baseline_pass'] and not x['candidate_pass'] for x in rows)}
    train=stats(splits['train']);hold=stats(splits['holdout'])
    baseline_unsafe=any(x['baseline_violations'] or x['baseline_critical'] for x in obs)
    safe=not baseline_unsafe and all(not s['candidate_policy_violations'] and not s['candidate_critical_regressions'] and s['delta_pass_rate']>=0 for s in [train,hold])
    improve=(train['delta_pass_rate']>0 and hold['delta_pass_rate']>0) or (train['mean_duration_delta_seconds']<0 and hold['mean_duration_delta_seconds']<0 and train['regressed_tasks']==0 and hold['regressed_tasks']==0)
    return {'kind':'paired_proposal','experiment_id':data['experiment_id'],'train':train,'holdout':hold,
            'decision':'PROPOSE_FOR_HUMAN_REVIEW' if safe and improve else 'REJECT_OR_MORE_EVIDENCE',
            'auto_apply':False,'independent_attestation':False,
            'caveat':'Datos pareados suministrados, sin inferencia estadística de superioridad ni atestación externa'}
