"""No live services, credentials, production systems or human review impersonation."""
import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from msa_runtime import core,observability
try:from msa_runtime import experiments
except ImportError:experiments=None
try:from msa_runtime import adaptive
except ImportError:adaptive=None


def observation(**updates):
    d={'execution_id':'run001','task_id':'A1','suite_id':'SYNTH01','strategy':'baseline','runtime':'codex','provenance':'synthetic','artifact_sha256':'a'*64,
       'tests_passed':9,'tests_total':10,'evidence_verified':4,'evidence_total':5,'handoffs_restored':1,'handoffs_attempted':1,
       'policy_violations':0,'critical_regressions':0,'duration_seconds':150.0,'cost_usd':None}
    d.update(updates);return d

class TestObservability(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.project=Path(self.tmp.name)/'repo';core.init(self.project,'synthetic','5.1.0')
    def test_ingest_summary(self):
        observability.ingest(self.project,observation())
        observability.ingest(self.project,observation(execution_id='run002',tests_passed=10,duration_seconds=50.0,provenance='manual'))
        r=observability.summary(self.project)
        self.assertEqual(r['by_strategy']['baseline']['executions'],2)
        self.assertAlmostEqual(r['by_strategy']['baseline']['test_pass_rate'],0.95)
        self.assertEqual(r['by_strategy']['baseline']['duration_median_seconds'],100.0)
        self.assertIsNone(r['by_strategy']['baseline']['cost_sum_usd'])
    def test_duplicate_execution_deny(self):
        observability.ingest(self.project,observation())
        with self.assertRaises(ValueError):observability.ingest(self.project,observation())
    def test_provenance_does_not_self_attest(self):
        with self.assertRaises(ValueError):observability.validate(observation(provenance='instrumented-attested'))
    def test_reject_extra_identifiers_and_secrets(self):
        with self.assertRaises(ValueError):observability.validate(observation(email='me@example.com'))
        with self.assertRaises(ValueError):observability.validate(observation(api_key='supersecret'))
    def test_reject_inf_nan_bool_and_bad_counts(self):
        for kw in ({'cost_usd':float('nan')},{'duration_seconds':float('inf')},{'tests_passed':True},{'evidence_verified':6}):
            with self.assertRaises(ValueError):observability.validate(observation(**kw))
    def test_calibration_requires_paired(self):
        core.append(self.project,'review',{'kind':'calibration','task_id':'A1','role':'self','score':4,'instrumented_evidence':False})
        self.assertIsNone(observability.calibration(self.project)['mean_absolute_error'])
        core.append(self.project,'review',{'kind':'calibration','task_id':'A1','role':'verifier','score':2,'instrumented_evidence':False})
        r=observability.calibration(self.project)
        self.assertEqual(r['mean_absolute_error'],2);self.assertEqual(r['independent_reviews_attested'],0)

@unittest.skipIf(experiments is None,'V5.2+')
class TestExperiments(unittest.TestCase):
    def config(self,alg='pso',budget=180):return {'function':'sphere','dimensions':3,'lower':-5,'upper':5,'budget':budget,'seed':42,'algorithm':alg}
    def test_deterministic_pso(self):
        a=experiments.optimize(self.config());b=experiments.optimize(self.config())
        self.assertEqual(a,b);self.assertEqual(a['evaluations'],180);self.assertFalse(a['external_effects'])
        self.assertLessEqual(a['best_value'],a['history'][0]);self.assertEqual(len(a['history']),180)
    def test_pso_uses_exact_budget_calls(self):
        calls=[0]
        original=experiments.FUNCTIONS['sphere']
        def instrumented(xs):
            calls[0]+=1
            return original(xs)
        experiments.FUNCTIONS['sphere']=instrumented
        try: result=experiments.optimize(self.config(budget=60))
        finally: experiments.FUNCTIONS['sphere']=original
        self.assertEqual(calls[0],result['evaluations'])
    def test_deterministic_random_and_bounded(self):
        a=experiments.optimize(self.config('random'));self.assertEqual(a,experiments.optimize(self.config('random')))
        self.assertTrue(all(-5<=x<=5 for x in a['best_position']))
    def test_reject_untrusted_objective(self):
        for diff in ({'function':'__import__'},{'algorithm':'exec'},{'budget':10000},{'seed':-1}):
            cfg=self.config();cfg.update(diff)
            with self.assertRaises(ValueError):experiments.optimize(cfg)
    def paired(self,candidate_good=True,viol=0):
        rows=[]
        for i in range(20):rows.append({'task_id':f'case{i:02}','split':'train' if i<10 else 'holdout',
            'baseline_pass':i%3!=0,'candidate_pass':True if candidate_good else False,
            'baseline_duration':100,'candidate_duration':80,'baseline_violations':0,'candidate_violations':viol,
            'baseline_critical':0,'candidate_critical':0})
        return {'experiment_id':'LAB01','observations':rows}
    def test_paired_positive_only_human_review(self):
        r=experiments.paired_analysis(self.paired());self.assertEqual(r['decision'],'PROPOSE_FOR_HUMAN_REVIEW')
        self.assertFalse(r['auto_apply']);self.assertFalse(r['independent_attestation'])
    def test_paired_regression_rejected(self):
        self.assertEqual(experiments.paired_analysis(self.paired(False))['decision'],'REJECT_OR_MORE_EVIDENCE')
        self.assertEqual(experiments.paired_analysis(self.paired(viol=1))['decision'],'REJECT_OR_MORE_EVIDENCE')
    def test_paired_holdout_minimum_and_duplicates(self):
        d=self.paired();d['observations'][-1]['task_id']='case00'
        with self.assertRaises(ValueError):experiments.paired_analysis(d)
        d=self.paired();
        for item in d['observations'][-6:]:item['split']='train'
        with self.assertRaises(ValueError):experiments.paired_analysis(d)

@unittest.skipIf(adaptive is None,'V6+')
class TestAdaptive(unittest.TestCase):
    def request(self,**kw):
        x={'task_id':'ATOM01','mode':'DELIVERY','risk':'low','complexity':'small','data_class':'synthetic','needs_external_write':False};x.update(kw);return x
    def test_low_risk_lite(self):
        x=adaptive.plan(self.request());self.assertEqual(x['strategy'],'LITE');self.assertFalse(x['promotion_allowed'])
    def test_unknown_fail_high(self):
        x=adaptive.plan(self.request(risk='unknown'));self.assertEqual(x['strategy'],'FULL_ADVERSARIAL');self.assertIn('independent_review_required',x['required_gates'])
    def test_external_write_not_authorized(self):
        x=adaptive.plan(self.request(needs_external_write=True));self.assertFalse(x['allowed_external_writes']);self.assertIn('explicit_external_authorization',x['required_gates'])
    def test_restricted_data_elevates(self):
        self.assertEqual(adaptive.plan(self.request(data_class='restricted'))['strategy'],'FULL_ADVERSARIAL')
    def test_experiment_proposal_does_not_change_gates(self):
        r=adaptive.plan(self.request(risk='high'),{'kind':'paired_proposal','experiment_id':'LAB02','decision':'PROPOSE_FOR_HUMAN_REVIEW','auto_apply':False})
        self.assertEqual(r['experiment_proposal']['recommendation'],'CANDIDATE_FOR_HUMAN_REVIEW')
        self.assertEqual(r['strategy'],'FULL_ADVERSARIAL')
        self.assertFalse(r['promotion_allowed'])
    def test_invalid_profile_rejected(self):
        with self.assertRaises(ValueError):adaptive.plan(self.request(risk='imaginary'))
        with self.assertRaises(ValueError):adaptive.plan(self.request(secret='abc'))

if __name__=='__main__':unittest.main()
