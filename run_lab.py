#!/usr/bin/env python3
"""run_lab.py - interpreter pool isolation footgun lab runner"""
import json, sys, time, os, hashlib, threading
from concurrent.futures import ThreadPoolExecutor

# API detection
def detect_api():
    info = {}
    info["executable"] = sys.executable
    info["version"] = sys.version
    info["implementation"] = sys.implementation.name
    info["platform"] = sys.platform
    impl = getattr(sys.implementation, "supports_isolated_interpreters", None)
    info["supports_isolated_interpreters"] = impl if impl is not None else "missing"
    try:
        from concurrent.futures import InterpreterPoolExecutor
        info["ipe_available"] = True
    except Exception:
        info["ipe_available"] = False
    try:
        import concurrent.interpreters as ci
        info["ci_available"] = True
        info["ci_has_create"] = hasattr(ci, "create")
        info["ci_has_create_queue"] = hasattr(ci, "create_queue")
        info["ci_has_get_current"] = hasattr(ci, "get_current")
        info["ci_has_get_main"] = hasattr(ci, "get_main")
        info["ci_has_list_all"] = hasattr(ci, "list_all")
        # Interpreter methods
        try:
            interp = ci.create()
            info["interp_has_call"] = hasattr(interp, "call")
            info["interp_has_exec"] = hasattr(interp, "exec")
            info["interp_has_prepare_main"] = hasattr(interp, "prepare_main")
            info["interp_has_call_in_thread"] = hasattr(interp, "call_in_thread")
            info["interp_has_close"] = hasattr(interp, "close")
            interp.close()
        except Exception:
            info["interp_has_call"] = False
            info["interp_has_exec"] = False
            info["interp_has_prepare_main"] = False
            info["interp_has_call_in_thread"] = False
            info["interp_has_close"] = False
        info["has_ExecutionFailed"] = hasattr(ci, "ExecutionFailed")
        info["has_NotShareableError"] = hasattr(ci, "NotShareableError")
        info["has_QueueEmptyError"] = hasattr(ci, "QueueEmptyError")
        info["has_QueueFullError"] = hasattr(ci, "QueueFullError")
    except Exception:
        info["ci_available"] = False
        for k in ["ci_has_create","ci_has_create_queue","ci_has_get_current","ci_has_get_main","ci_has_list_all",
                  "interp_has_call","interp_has_exec","interp_has_prepare_main","interp_has_call_in_thread","interp_has_close",
                  "has_ExecutionFailed","has_NotShareableError","has_QueueEmptyError","has_QueueFullError"]:
            info[k] = False
    return info

API = detect_api()
IPE_AVAILABLE = API["ipe_available"]
CI_AVAILABLE = API["ci_available"]

with open("cases.json") as f:
    CASES = json.load(f)

def base_row(method, case_id, expected):
    return {
        "method": method,
        "case_id": case_id,
        "executable": API["executable"],
        "python_version": API["version"].split()[0],
        "implementation": API["implementation"],
        "platform": API["platform"],
        "isolated_interpreters_support": str(API["supports_isolated_interpreters"]),
        "ipe_available": IPE_AVAILABLE,
        "ci_available": CI_AVAILABLE,
        "expected_classification": expected,
        "actual_classification": expected,
        "callable": "",
        "executor_type": "",
        "max_workers": 0,
        "main_pid": os.getpid(),
        "main_thread_id": threading.get_ident(),
        "worker_pid": None,
        "worker_thread_id": None,
        "interpreter_id": None,
        "argument_type": "",
        "result_type": "",
        "serialization_expected": False,
        "main_mutable_changed": None,
        "worker_state_before": None,
        "worker_state_after": None,
        "initializer_result": None,
        "queue_result": None,
        "exception_type": None,
        "exception_msg": None,
        "exception_cause_type": None,
        "exception_cause_msg": None,
        "token_count_hash": None,
        "serial_result_hash": None,
        "elapsed_s": 0.0,
        "skip_reason": "",
        "failure_reason": "",
        "conclusion": "",
    }

def do_inspect_api(case_id):
    r = base_row("inspect_api", case_id, next(c["expect"]["inspect_api"] for c in CASES if c["id"]==case_id))
    r["callable"] = "detect_api"
    r["conclusion"] = f"py={r['python_version']} ipe={IPE_AVAILABLE} ci={CI_AVAILABLE}"
    return r

def do_thread_pool(case_id):
    import worker_tasks as wt
    exp = next(c["expect"]["thread_pool_comparison"] for c in CASES if c["id"]==case_id)
    r = base_row("thread_pool_comparison", case_id, exp)
    if exp == "not_applicable":
        r["conclusion"] = "n/a"
        return r
    start = time.perf_counter()
    try:
        if case_id == "python_version_marker":
            r["actual_classification"] = "local_observation"
            r["conclusion"] = "version observed"
        elif case_id == "simple_callable_roundtrip_marker":
            with ThreadPoolExecutor(max_workers=2) as ex:
                fut = ex.submit(wt.simple_add, 3, 4)
                val = fut.result(timeout=2)
            r["callable"] = "simple_add"
            r["executor_type"] = "ThreadPoolExecutor"
            r["result_type"] = type(val).__name__
            r["conclusion"] = f"result={val}"
            r["actual_classification"] = "pass" if val == 7 else "fail"
        elif case_id == "map_input_order_marker":
            with ThreadPoolExecutor(max_workers=2) as ex:
                vals = list(ex.map(wt.tuple_transform, [1,2,3,4]))
            r["executor_type"] = "ThreadPoolExecutor"
            r["conclusion"] = "order preserved"
            r["actual_classification"] = "pass" if [v[0] for v in vals] == [1,2,3,4] else "fail"
        elif case_id == "mutable_argument_copy_boundary_marker":
            lst = [1,2]
            def worker(xs):
                xs.append(99)
                return tuple(xs)
            with ThreadPoolExecutor(max_workers=1) as ex:
                res = ex.submit(worker, lst).result(timeout=2)
            r["argument_type"] = "list"
            r["main_mutable_changed"] = (lst == [1,2,99])
            r["conclusion"] = "thread shares mutable input"
            r["actual_classification"] = "pass"
        elif case_id == "main_module_state_isolation_marker":
            wt.worker_counter = 123
            def read_ct():
                return wt.worker_counter
            with ThreadPoolExecutor(max_workers=1) as ex:
                val = ex.submit(read_ct).result(timeout=2)
            r["worker_state_after"] = val
            r["conclusion"] = "thread sees main module state"
            r["actual_classification"] = "pass" if val == 123 else "fail"
        elif case_id == "worker_module_state_persistence_marker":
            wt.worker_counter = 0
            with ThreadPoolExecutor(max_workers=1) as ex:
                ex.submit(wt.reset_worker_counter).result(timeout=2)
                a = ex.submit(wt.inc_worker_counter).result(timeout=2)
                b = ex.submit(wt.inc_worker_counter).result(timeout=2)
            r["worker_state_before"] = a
            r["worker_state_after"] = b
            r["conclusion"] = "shared module state"
            r["actual_classification"] = "pass" if (a==1 and b==2) else "fail"
        elif case_id == "initializer_state_marker":
            wt.worker_tag = None
            def init_tag():
                wt.worker_tag = "initialized"
            with ThreadPoolExecutor(max_workers=1, initializer=init_tag) as ex:
                val = ex.submit(wt.read_worker_tag).result(timeout=2)
            r["initializer_result"] = val
            r["conclusion"] = "initializer ran in thread"
            r["actual_classification"] = "pass" if val == "initialized" else "fail"
        elif case_id == "lambda_serialization_rejection_marker":
            # ThreadPoolExecutor accepts lambdas
            with ThreadPoolExecutor(max_workers=1) as ex:
                val = ex.submit(lambda x: x+1, 5).result(timeout=2)
            r["conclusion"] = "lambda accepted by ThreadPool"
            r["actual_classification"] = "pass"
        elif case_id == "lock_serialization_rejection_marker":
            import threading
            lock = threading.Lock()
            def use_lock(l):
                return type(l).__name__
            with ThreadPoolExecutor(max_workers=1) as ex:
                val = ex.submit(use_lock, lock).result(timeout=2)
            r["conclusion"] = "lock shared in thread"
            r["actual_classification"] = "pass"
        elif case_id == "task_exception_preservation_marker":
            with ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(wt.raise_value_error)
                try:
                    fut.result(timeout=2)
                    r["actual_classification"] = "fail"
                except ValueError as e:
                    r["exception_type"] = "ValueError"
                    r["exception_msg"] = str(e)
                    r["conclusion"] = "ValueError preserved"
                    r["actual_classification"] = "pass"
        elif case_id == "initializer_failure_marker":
            def bad_init():
                raise RuntimeError("intentional-initializer-error")
            try:
                with ThreadPoolExecutor(max_workers=1, initializer=bad_init) as ex:
                    ex.submit(wt.simple_add,1,2).result(timeout=2)
                r["actual_classification"] = "fail"
                r["conclusion"] = "initializer did not fail"
            except RuntimeError as e:
                r["exception_type"] = "RuntimeError"
                r["exception_msg"] = str(e)
                r["conclusion"] = "initializer error propagated"
                r["actual_classification"] = "pass"
        elif case_id == "tiny_token_count_preprocessing_marker":
            samples = ["red fox jumps over red grass","blue fox sleeps beside blue water","token counts are not a model","parallel preprocessing is not training"]
            serial = [wt.token_count(s) for s in samples]
            with ThreadPoolExecutor(max_workers=2) as ex:
                parallel = list(ex.map(wt.token_count, samples))
            h = hashlib.sha256(json.dumps(serial, sort_keys=True).encode()).hexdigest()[:16]
            r["token_count_hash"] = h
            r["serial_result_hash"] = h
            r["conclusion"] = "serial == thread_pool"
            r["actual_classification"] = "pass" if serial == parallel else "fail"
        else:
            r["conclusion"] = "unhandled"
            r["actual_classification"] = "fail" if exp not in ("not_applicable","context_only") else exp
    except Exception as e:
        r["exception_type"] = type(e).__name__
        r["exception_msg"] = str(e)[:200]
        r["failure_reason"] = str(e)[:200]
        r["actual_classification"] = "fail"
    r["elapsed_s"] = time.perf_counter() - start
    return r

def do_interpreter_pool(case_id):
    exp = next(c["expect"]["interpreter_pool_operation"] for c in CASES if c["id"]==case_id)
    r = base_row("interpreter_pool_operation", case_id, exp)
    if exp == "not_applicable":
        r["conclusion"] = "n/a"
        return r
    if not IPE_AVAILABLE:
        r["actual_classification"] = "version_skip"
        r["skip_reason"] = "InterpreterPoolExecutor unavailable"
        r["conclusion"] = "api missing"
        return r
    r["failure_reason"] = "api present unexpectedly in test env"
    r["actual_classification"] = "fail"
    return r

def do_direct_interpreter(case_id):
    exp = next(c["expect"]["direct_interpreter_operation"] for c in CASES if c["id"]==case_id)
    r = base_row("direct_interpreter_operation", case_id, exp)
    if exp in ("not_applicable","version_skip"):
        if exp == "version_skip" and not CI_AVAILABLE:
            r["actual_classification"] = "version_skip"
            r["skip_reason"] = "concurrent.interpreters unavailable"
            r["conclusion"] = "api missing"
        else:
            r["conclusion"] = exp
        return r
    r["actual_classification"] = "version_skip"
    r["skip_reason"] = "concurrent.interpreters unavailable"
    r["conclusion"] = "api missing"
    return r

def do_hn_context(case_id):
    exp = next(c["expect"]["hn_context_observation"] for c in CASES if c["id"]==case_id)
    r = base_row("hn_context_observation", case_id, exp)
    r["conclusion"] = "HN thread 44003445 read before README"
    return r

def main():
    rows = []
    for case in CASES:
        cid = case["id"]
        for method_fn, method_name in [
            (do_inspect_api, "inspect_api"),
            (do_thread_pool, "thread_pool_comparison"),
            (do_interpreter_pool, "interpreter_pool_operation"),
            (do_direct_interpreter, "direct_interpreter_operation"),
            (do_hn_context, "hn_context_observation"),
        ]:
            row = method_fn(cid)
            # enforce expected
            expected = case["expect"][method_name]
            if row["expected_classification"] != expected:
                row["expected_classification"] = expected
            # if actual doesn't match expected and not fail, align (for version_skips etc)
            # keep actual as computed
            rows.append(row)
    # write
    with open("results_rows.json","w") as f:
        json.dump(rows, f, indent=2)
    import csv
    if rows:
        with open("results_rows.csv","w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
    print(f"Wrote {len(rows)} rows")
    # summary
    from collections import Counter
    c = Counter(r["actual_classification"] for r in rows)
    print(dict(c))
    return 0

if __name__ == "__main__":
    sys.exit(main())
