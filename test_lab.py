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
    def test_expected_equals_actual(self):
        bad = [(r["case_id"], r["method"], r["expected_classification"], r["actual_classification"]) for r in self.rows if r["expected_classification"] != r["actual_classification"]]
        self.assertEqual(bad, [], f"mismatches: {bad}")
    # behavior checks - thread_pool
    def test_simple_callable_tp(self):
        r = [x for x in self.rows if x["case_id"]=="simple_callable_roundtrip_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_map_order_tp(self):
        r = [x for x in self.rows if x["case_id"]=="map_input_order_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_mutable_copy_tp(self):
        r = [x for x in self.rows if x["case_id"]=="mutable_argument_copy_boundary_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_module_state_tp(self):
        r = [x for x in self.rows if x["case_id"]=="main_module_state_isolation_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_worker_persistence_tp(self):
        r = [x for x in self.rows if x["case_id"]=="worker_module_state_persistence_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_initializer_tp(self):
        r = [x for x in self.rows if x["case_id"]=="initializer_state_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_exception_tp(self):
        r = [x for x in self.rows if x["case_id"]=="task_exception_preservation_marker" and x["method"]=="thread_pool_comparison"][0]
        self.assertEqual(r["actual_classification"], "pass")
        self.assertIn("ValueError", r["exception_type"] or "")
    # behavior checks - interpreter_pool
    def test_simple_callable_ip(self):
        r = [x for x in self.rows if x["case_id"]=="simple_callable_roundtrip_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_map_order_ip(self):
        r = [x for x in self.rows if x["case_id"]=="map_input_order_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_mutable_copy_ip(self):
        r = [x for x in self.rows if x["case_id"]=="mutable_argument_copy_boundary_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
        # main_mutable_changed should be False (copy boundary)
        self.assertFalse(r["main_mutable_changed"])
    def test_module_isolation_ip(self):
        r = [x for x in self.rows if x["case_id"]=="main_module_state_isolation_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_worker_persistence_ip(self):
        r = [x for x in self.rows if x["case_id"]=="worker_module_state_persistence_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_initializer_ip(self):
        r = [x for x in self.rows if x["case_id"]=="initializer_state_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_lock_rejection_ip(self):
        r = [x for x in self.rows if x["case_id"]=="lock_serialization_rejection_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "expected_error")
        self.assertTrue(r["exception_type"])
    def test_exception_ip(self):
        r = [x for x in self.rows if x["case_id"]=="task_exception_preservation_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_initializer_failure_ip(self):
        r = [x for x in self.rows if x["case_id"]=="initializer_failure_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "expected_error")
    def test_preprocessing_ip(self):
        r = [x for x in self.rows if x["case_id"]=="tiny_token_count_preprocessing_marker" and x["method"]=="interpreter_pool_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
        self.assertTrue(r["token_count_hash"])
    # direct_interpreter
    def test_direct_lifecycle(self):
        r = [x for x in self.rows if x["case_id"]=="direct_interpreter_lifecycle_marker" and x["method"]=="direct_interpreter_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_builtins_isolation(self):
        r = [x for x in self.rows if x["case_id"]=="direct_interpreter_builtin_isolation_marker" and x["method"]=="direct_interpreter_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_queue_roundtrip(self):
        r = [x for x in self.rows if x["case_id"]=="cross_interpreter_queue_roundtrip_marker" and x["method"]=="direct_interpreter_operation"][0]
        self.assertEqual(r["actual_classification"], "pass")
    def test_queue_unshareable(self):
        r = [x for x in self.rows if x["case_id"]=="queue_unshareable_object_rejection_marker" and x["method"]=="direct_interpreter_operation"][0]
        self.assertEqual(r["actual_classification"], "expected_error")
    # no global claims
    def test_no_global_claims(self):
        for fname in ["README.md","RESULTS.md"]:
            try:
                with open(fname) as f: txt = f.read().lower()
                for bad in ["speedup proven","ml validated","secure sandbox","numpy compatible","pytorch compatible","training faster"]:
                    self.assertNotIn(bad, txt, f"{fname} contains {bad}")
            except FileNotFoundError: pass
    # artifact cleanliness
    def test_artifacts_clean(self):
        import glob, re
        files = ["README.md","RESULTS.md","cases.json","results_rows.json","results_rows.csv"]
        for pat in ["hn_*.json","hn_*.md","VERIFY.md"]:
            files += glob.glob(pat)
        # allow /tmp/ip_lab in results_rows (executable path) – but not tokens/session ids
        bad_re = re.compile(r"ghp_[A-Za-z0-9]{20,}|openclaw.*session|/home/ubuntu/\.openclaw", re.I)
        for fn in set(files):
            try:
                with open(fn) as f: txt=f.read()
                m = bad_re.search(txt)
                self.assertIsNone(m, f"{fn} contains prohibited: {m.group(0) if m else ''}")
            except FileNotFoundError: pass

if __name__ == "__main__": unittest.main()
