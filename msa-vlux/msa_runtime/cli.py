"""MSA portable CLI, no dependencies. Deliberately no remote-write commands."""
import argparse,json,sys
from pathlib import Path
from . import core,evaluation

ROOT=Path(__file__).resolve().parents[1]
VERSION=(ROOT/'VERSION').read_text(encoding='utf-8').strip()

def main(argv=None):
    p=argparse.ArgumentParser(prog='msa',description='MSA-VLUX portable workflow (no external writes)')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    sub.add_parser('verify-package')
    a=sub.add_parser('init');a.add_argument('--project-dir',required=True);a.add_argument('--name',required=True)
    a=sub.add_parser('status');a.add_argument('--project-dir',required=True)
    a=sub.add_parser('set-atom');a.add_argument('--project-dir',required=True);a.add_argument('--id',required=True);a.add_argument('--mode',required=True);a.add_argument('--status',required=True);a.add_argument('--baseline-sha')
    a=sub.add_parser('record');a.add_argument('--project-dir',required=True);a.add_argument('--type',required=True);a.add_argument('--actor',default='agent');a.add_argument('--data-file',required=True)
    a=sub.add_parser('verify-ledger');a.add_argument('--project-dir',required=True)
    a=sub.add_parser('eval');a.add_argument('--scenarios',default=str(ROOT/'evals/scenarios.json'));a.add_argument('--traces',required=True);a.add_argument('--output')
    a=sub.add_parser('assess');a.add_argument('--project-dir',required=True);a.add_argument('--input',required=True);a.add_argument('--output')
    a=sub.add_parser('gate');a.add_argument('--action',required=True);a.add_argument('--project-dir',required=True)
    if VERSION in ('4.2.0','5.0.0'):
        a=sub.add_parser('handoff');a.add_argument('--project-dir',required=True);a.add_argument('--output',required=True);a.add_argument('--runtime',required=True);a.add_argument('--include',action='append',default=[],help='Ruta de evidencia UTF-8 autorizada bajo --project-dir; repetible')
        a=sub.add_parser('verify-handoff');a.add_argument('--archive',required=True)
        a=sub.add_parser('import-handoff');a.add_argument('--archive',required=True);a.add_argument('--target',required=True)
        a=sub.add_parser('resume');a.add_argument('--project-dir',required=True)
        a=sub.add_parser('role-packet');a.add_argument('--project-dir',required=True);a.add_argument('--role',required=True);a.add_argument('--master-execution-id',required=True);a.add_argument('--output',required=True)
        a=sub.add_parser('check-review');a.add_argument('--packet',required=True);a.add_argument('--review',required=True)
    if VERSION=='5.0.0':
        a=sub.add_parser('improve');a.add_argument('--baseline',required=True);a.add_argument('--candidate',required=True);a.add_argument('--holdout',required=True);a.add_argument('--output')
    args=p.parse_args(argv)
    try:
        c=args.command
        if c=='doctor':result=core.doctor(ROOT,VERSION)
        elif c=='verify-package':result=core.verify_package(ROOT)
        elif c=='init':result=core.init(args.project_dir,args.name,VERSION)
        elif c=='status':core.check_chain(args.project_dir);result=core.load_state(args.project_dir)
        elif c=='set-atom':result=core.set_atom(args.project_dir,args.id,args.mode,args.status,args.baseline_sha)
        elif c=='record':result=core.append(args.project_dir,args.type,core.read(args.data_file),args.actor)
        elif c=='verify-ledger':result=core.check_chain(args.project_dir)
        elif c=='eval':result=evaluation.evaluate(args.scenarios,args.traces)
        elif c=='assess':result=evaluation.self_assess(args.project_dir,args.input)
        elif c=='gate':
            # Advisory check intentionally deny-all: without out-of-band enforcement this MUST NOT claim authorization.
            result={'action':args.action,'allowed':False,'reason':'External effects require separate human approval and independently enforced runtime permissions; no approval travels with a handoff'}
        elif c in ('handoff','verify-handoff','import-handoff','resume'):
            from . import continuity
            if c=='handoff':result=continuity.build_handoff(args.project_dir,args.output,args.runtime,args.include)
            elif c=='verify-handoff':result=continuity.verify_handoff(args.archive)
            elif c=='import-handoff':result=continuity.import_handoff(args.archive,args.target)
            else:
                result=continuity.resume_report(args.project_dir)
                result['runtime_version']=VERSION
                result['project_origin_version']=result['msa_version']
        elif c=='role-packet':
            from . import delegation
            result=delegation.make_packet(args.project_dir,args.role,args.output,args.master_execution_id)
        elif c=='check-review':
            from . import delegation
            result=delegation.check_review(args.packet,args.review)
        elif c=='improve':
            from . import improvement
            result=improvement.recommend(args.baseline,args.candidate,args.holdout)
        else:raise ValueError('Operación no reconocida')
        data=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)
        if c in ('eval','assess','improve') and getattr(args,'output',None):
            outfile=Path(args.output)
            if outfile.exists():raise FileExistsError('Archivo de salida existente: no sobrescrito')
            core.atomic_write(outfile,data.encode())
        print(data)
        return 0 if c!='eval' or result['failed']==0 else 1
    except (ValueError,KeyError,FileNotFoundError,FileExistsError,PermissionError) as ex:
        print('MSA ERROR: '+str(ex),file=sys.stderr)
        return 2

if __name__=='__main__':sys.exit(main())
