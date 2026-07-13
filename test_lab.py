import unittest, json
class TestLab(unittest.TestCase):
    def setUp(self):
        with open("cases.json") as f:
            self.cases = json.load(f)
        with open("results_rows.json") as f:
            self.rows = json.load(f)
    def test_case_count(self):
        self.assertEqual(len(self.cases), 20)
    def test_markers_exist(self):
        ids = [c["id"] for c in self.cases]
        expected = ["python_version_marker","isolated_interpreters_support_marker","interpreter_pool_executor_available_marker","concurrent_interpreters_available_marker","simple_callable_roundtrip_marker","map_input_order_marker","mutable_argument_copy_boundary_marker","main_module_state_isolation_marker","worker_module_state_persistence_marker","initializer_state_marker","lambda_serialization_rejection_marker","lock_serialization_rejection_marker","task_exception_preservation_marker","initializer_failure_marker","direct_interpreter_lifecycle_marker","direct_interpreter_builtin_isolation_marker","cross_interpreter_queue_roundtrip_marker","queue_unshareable_object_rejection_marker","tiny_token_count_preprocessing_marker","no_global_speedup_security_or_ml_claim_marker"]
        for e in expected:
            self.assertEqual(ids.count(e), 1, e)
    def test_100_rows(self):
        self.assertEqual(len(self.rows), 100)
    def test_pairs_unique(self):
        pairs = [(r["method"], r["case_id"]) for r in self.rows]
        self.assertEqual(len(set(pairs)), 100)
    def test_classifications_allowed(self):
        allowed = {"pass","expected_error","local_observation","version_skip","context_only","not_applicable","fail"}
        for r in self.rows:
            self.assertIn(r["expected_classification"], allowed)
            self.assertIn(r["actual_classification"], allowed)
            self.assertTrue(r["expected_classification"])
            self.assertTrue(r["actual_classification"])
    def test_na_pairs(self):
        for r in self.rows:
            if r["expected_classification"] == "not_applicable":
                self.assertEqual(r["actual_classification"], "not_applicable")
    def test_expected_equals_actual_or_fail(self):
        for r in self.rows:
            self.assertTrue(r["expected_classification"] == r["actual_classification"] or r["actual_classification"] == "fail")
    def test_simple_callable(self):
        # just verify row exists and passed or version_skip
        rows = [r for r in self.rows if r["case_id"]=="simple_callable_roundtrip_marker" and r["method"]=="thread_pool_comparison"]
        self.assertEqual(len(rows),1)
        self.assertIn(rows[0]["actual_classification"], ("pass","version_skip"))
    def test_map_order(self):
        rows = [r for r in self.rows if r["case_id"]=="map_input_order_marker" and r["method"]=="thread_pool_comparison"]
        self.assertEqual(rows[0]["actual_classification"], "pass")
    def test_no_global_claims(self):
        for fname in ["README.md","RESULTS.md"]:
            try:
                with open(fname) as f:
                    txt = f.read().lower()
                bad = ["speedup proven","ml validated","secure sandbox","numpy compatible","pytorch compatible","training faster"]
                for b in bad:
                    self.assertNotIn(b, txt, f"{fname} contains {b}")
            except FileNotFoundError:
                pass
    def test_artifacts_clean(self):
        import glob, re
        files = ["README.md","RESULTS.md","cases.json","results_rows.json"]
        for pat in ["hn_*.json","hn_*.md"]:
            files += glob.glob(pat)
        bad_re = re.compile(r"/home/ubuntu|ghp_|openclaw|/tmp/ip_lab")
        for fn in files:
            try:
                with open(fn) as f: txt=f.read()
                self.assertIsNone(bad_re.search(txt), f"{fn} contains prohibited string")
            except FileNotFoundError: pass

if __name__ == "__main__": unittest.main()
