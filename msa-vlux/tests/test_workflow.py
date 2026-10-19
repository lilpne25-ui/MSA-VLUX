"""Proves behavior of portable tools, not model compliance or OS sandbox security."""
import copy,hashlib,json,os,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from msa_runtime import core,evaluation

class TestLedger(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.p=Path(self.t.name)/'workspace';self.p.mkdir()
        self.state=core.init(self.p,'proyecto ficticio','4.1.0')
    def test_init_never_overwrite(self):
        with self.assertRaises(FileExistsError):core.init(self.p,'duplicate','4.1.0')
    def test_ledger_integrity_and_tampering(self):
        e=core.append(self.p,'evidence',{'result':'PASS','artifact_sha256':'0'*64})
        self.assertEqual(core.check_chain(self.p)['events'],1)
        text=(core.root(self.p)/'history.jsonl').read_text()
        (core.root(self.p)/'history.jsonl').write_text(text.replace('PASS','FAKE'))
        with self.assertRaises(ValueError):core.check_chain(self.p)
    def test_no_secrets_in_events(self):
        for x in [{'password':'ABCD'},{'message':'Bearer SECRETSECRET'},{'api_key':'123456'}]:
            with self.assertRaises(ValueError):core.append(self.p,'evidence',x)
    def test_role_decisions_are_not_remote_authorizations(self):
        s=core.set_atom(self.p,'A01','AUDIT','in_progress',baseline='abcdef0')
        self.assertEqual(s['mode'],'AUDIT')
        self.assertFalse(core.load_state(self.p)['external_write_authorized'])
    def test_assessment_requires_real_event_id(self):
        e=core.append(self.p,'evidence',{'label':'synthetic test','result':'PASS','artifact_sha256':'a'*64})
        template=json.loads((ROOT/'templates/SELF-ASSESSMENT.json').read_text())
        template['dimensions']['accuracy']={'score':4,'evidence_ids':[e['id']],'claim':'verified by fixture'}
        inp=self.p/'assessment.json';inp.write_text(json.dumps(template))
        score=evaluation.self_assess(self.p,inp)
        self.assertEqual(score['score'],14)
        self.assertEqual(score['human_review'],'not_verified')
        template['dimensions']['accuracy']['evidence_ids']=['nonexistent']
        inp.write_text(json.dumps(template))
        with self.assertRaises(ValueError):evaluation.self_assess(self.p,inp)
    def test_assessment_high_score_cannot_lack_evidence(self):
        t=json.loads((ROOT/'templates/SELF-ASSESSMENT.json').read_text());t['dimensions']['accuracy']['score']=4
        inp=self.p/'a.json';inp.write_text(json.dumps(t))
        with self.assertRaises(ValueError):evaluation.self_assess(self.p,inp)
    def test_allowlisted_event_types_only(self):
        with self.assertRaises(ValueError):core.append(self.p,'git_push',{})
    def test_eval_compliant_and_adversarial(self):
        good=evaluation.evaluate(ROOT/'evals/scenarios.json',ROOT/'evals/traces-pass.json')
        bad=evaluation.evaluate(ROOT/'evals/scenarios.json',ROOT/'evals/traces-fail.json')
        self.assertEqual(good['failed'],0);self.assertEqual(bad['failed'],6)
    def test_manifest_if_present(self):
        if (ROOT/'SHA256SUMS.txt').exists():
            self.assertTrue(core.verify_package(ROOT)['verified'])
    def test_cli_gate_default_denies(self):
        cmd=[sys.executable,str(ROOT/'scripts/msa.py'),'gate','--action','push','--project-dir',str(self.p)]
        o=subprocess.run(cmd,capture_output=True,text=True,check=True)
        self.assertFalse(json.loads(o.stdout)['allowed'])

class TestHandoff(unittest.TestCase):
    def setUp(self):
        try:from msa_runtime import continuity
        except ImportError:self.skipTest('Handoff begins in 4.2')
        self.continuity=continuity
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.p=Path(self.t.name)/'a';self.p.mkdir();core.init(self.p,'ficticio','4.2.0')
        core.append(self.p,'evidence',{'label':'sin datos de clientes','result':'PASS'})
        core.set_atom(self.p,'A2','AUDIT','in_progress','abc123')
        self.bundle=Path(self.t.name)/'handoff.zip'
    def test_roundtrip_and_no_approvals(self):
        c=self.continuity
        meta=c.build_handoff(self.p,self.bundle,'codex')
        self.assertTrue(meta['sha256']);self.assertTrue(c.verify_handoff(self.bundle)['verified'])
        target=Path(self.t.name)/'next-runtime';c.import_handoff(self.bundle,target)
        self.assertEqual(core.check_chain(target)['events'],2)
        self.assertFalse(core.load_state(target)['external_write_authorized'])
        self.assertEqual(c.resume_report(target)['baseline_sha'],'abc123')
        with self.assertRaises(FileExistsError):c.import_handoff(self.bundle,target)
    def test_opt_in_evidence_survives_and_secret_is_blocked(self):
        c=self.continuity
        evidence=self.p/'evidence.md';evidence.write_text('Resultado sintético de pruebas')
        c.build_handoff(self.p,self.bundle,'codex',includes=['evidence.md'])
        target=Path(self.t.name)/'restored';c.import_handoff(self.bundle,target)
        self.assertEqual((core.root(target)/'imported-evidence/evidence.md').read_text(),'Resultado sintético de pruebas')
        secret=self.p/'danger.log';secret.write_text('Authorization: Bearer NOT-REAL-KEY')
        with self.assertRaises(ValueError):c.build_handoff(self.p,Path(self.t.name)/'fail.zip','codex',includes=['danger.log'])
    def test_outside_project_rejected(self):
        c=self.continuity
        foreign=Path(self.t.name)/'outside.txt';foreign.write_text('not permitted')
        with self.assertRaises(ValueError):c.build_handoff(self.p,self.bundle,'codex',includes=[str(foreign)])
    def test_reject_tampered_zip(self):
        c=self.continuity;c.build_handoff(self.p,self.bundle,'claude-cloud')
        original=zipfile.ZipFile(self.bundle)
        new=Path(self.t.name)/'tampered.zip'
        with zipfile.ZipFile(new,'w') as z:
            for n in original.namelist():
                d=original.read(n)
                if n=='state/history.jsonl':d=d.replace(b'PASS',b'FAIL')
                z.writestr(n,d)
        original.close()
        with self.assertRaises(ValueError):c.verify_handoff(new)
    def test_reject_extra_archive_files(self):
        c=self.continuity;c.build_handoff(self.p,self.bundle,'codex')
        with zipfile.ZipFile(self.bundle,'a') as z:z.writestr('private.env','verybad')
        with self.assertRaises(ValueError):c.verify_handoff(self.bundle)
    def test_no_unapproved_evidence_files_collected(self):
        c=self.continuity
        secret=self.p/'secret.env';secret.write_text('FAKE_SECRET=do-not-transfer')
        c.build_handoff(self.p,self.bundle,'codex')
        with zipfile.ZipFile(self.bundle) as z:
            self.assertNotIn('secret.env',z.namelist())
            self.assertNotIn(b'FAKE_SECRET',b''.join(z.read(k) for k in z.namelist()))

class TestDelegation(unittest.TestCase):
    def setUp(self):
        try:from msa_runtime import delegation
        except ImportError:self.skipTest('Delegation begins in V4.2')
        self.d=delegation
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.p=Path(self.t.name)/'workspace';self.p.mkdir()
        core.init(self.p,'trabajo ficticio','4.2.0')
        core.set_atom(self.p,'A1','AUDIT','in_progress','a'*40)
        self.packet=Path(self.t.name)/'packet.json';self.review=Path(self.t.name)/'review.json'
        self.d.make_packet(self.p,'verifier',self.packet,'master0001')
    def test_role_packet_and_independence_claim(self):
        payload={'reviewer_execution_id':'reviewer0002','master_execution_id':'master0001',
                 'role':'verifier','artifact_sha':'a'*40,'findings':[],'result':'PASS_REPORTED','independence_declared':True}
        self.review.write_text(json.dumps(payload))
        checked=self.d.check_review(self.packet,self.review)
        self.assertEqual(checked['status'],'DECLARED_INDEPENDENT_NOT_ATTESTED')
        payload['reviewer_execution_id']='master0001'
        self.review.write_text(json.dumps(payload))
        with self.assertRaises(ValueError):self.d.check_review(self.packet,self.review)
    def test_role_wrong_sha_rejected(self):
        payload={'reviewer_execution_id':'reviewer0002','master_execution_id':'master0001',
                 'role':'verifier','artifact_sha':'bad','findings':[],'result':'PASS_REPORTED','independence_declared':True}
        self.review.write_text(json.dumps(payload))
        with self.assertRaises(ValueError):self.d.check_review(self.packet,self.review)

class TestImprovement(unittest.TestCase):
    def setUp(self):
        try:from msa_runtime import improvement
        except ImportError:self.skipTest('Improvement begins in v5')
        self.m=improvement
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
    def file(self,name,rate=0.8,coverage=0.8,recovery=0.8,duration=300,violations=0,crit=0,suite='S',baseline=None):
        path=Path(self.t.name)/f'{name}.json'
        data={'sample_count':20,'trace_sha256':hashlib.sha256(name.encode()).hexdigest(),
              'suite_id':suite,'pass_rate':rate,'evidence_coverage':coverage,'recovery_rate':recovery,
              'duration_seconds':duration,'policy_violations':violations,'critical_regressions':crit}
        if baseline:data['holdout_baseline']=baseline
        path.write_text(json.dumps(data))
        return path,data
    def test_improvement_requires_holdout(self):
        b,_=self.file('baseline');c,_=self.file('candidate',rate=0.9)
        h,_=self.file('holdout',rate=0.9,suite='H')
        with self.assertRaises(ValueError):self.m.recommend(b,c,h)
    def test_improvement_with_holdout_is_only_proposal(self):
        b,_=self.file('baseline');c,_=self.file('candidate',rate=0.9)
        h0,hd=self.file('holdout_before',suite='H')
        h,_=self.file('holdout_after',rate=0.9,suite='H',baseline=hd)
        result=self.m.recommend(b,c,h)
        self.assertEqual(result['decision'],'PROPOSE_FOR_HUMAN_REVIEW')
        self.assertFalse(result['auto_apply'])
    def test_policy_regression_blocks_speed_gain(self):
        b,_=self.file('baseline');c,_=self.file('candidate',rate=0.95,duration=100,violations=1)
        _,hd=self.file('holdout_before',suite='H')
        h,_=self.file('holdout_after',rate=0.95,suite='H',baseline=hd)
        result=self.m.recommend(b,c,h)
        self.assertEqual(result['decision'],'REJECT_OR_MORE_EVIDENCE')
    def test_holdout_regression_blocks(self):
        b,_=self.file('baseline');c,_=self.file('candidate',rate=0.95)
        _,hd=self.file('holdout_before',suite='H')
        h,_=self.file('holdout_after',rate=0.65,suite='H',baseline=hd)
        self.assertEqual(self.m.recommend(b,c,h)['decision'],'REJECT_OR_MORE_EVIDENCE')

if __name__=='__main__':unittest.main()
