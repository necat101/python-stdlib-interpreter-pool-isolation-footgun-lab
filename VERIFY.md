# VERIFY

Repository: https://github.com/necat101/python-stdlib-interpreter-pool-isolation-footgun-lab

Verified implementation commit: d2c713d164e92f502a291ae7126ba9bda4e024df

This is a v2 repair. The original v1 (2b55e0e / 312ec2b) was a Python 3.12 skip-path scaffold with stubbed InterpreterPoolExecutor / concurrent.interpreters implementations. v2 implements the full interpreter-pool and direct-interpreter behavior under Python 3.14.6.

Clone command:
```
git clone https://github.com/necat101/python-stdlib-interpreter-pool-isolation-footgun-lab.git
cd python-stdlib-interpreter-pool-isolation-footgun-lab
git checkout d2c713d164e92f502a291ae7126ba9bda4e024df
```

Python executable: /home/ubuntu/.local/bin/python3.14
Python version: 3.14.6
Implementation: cpython
Platform: linux

API availability:
- supports_isolated_interpreters: True
- InterpreterPoolExecutor available: True
- concurrent.interpreters available: True

Validation commands:
```
~/.local/bin/python3.14 -m py_compile run_lab.py worker_tasks.py test_lab.py
# exit code: 0

~/.local/bin/python3.14 run_lab.py
# exit code: 0
# Wrote 100 rows

~/.local/bin/python3.14 -m unittest -v
# exit code: 0
# Ran 30 tests – OK
```

Unittest count: 30
Cases: 20
Methods: 5
Rows: 100

Classification counts:
- pass: 32
- expected_error: 3
- local_observation: 2
- context_only: 20
- not_applicable: 43
- fail: 0
- version_skip: 0

Interpreter-pool: 9 pass, 2 expected_error (lock serialization rejection, initializer failure)
Direct-interpreter: 3 pass, 1 expected_error (queue unshareable object)
Thread-pool: 11 pass
Preprocessing: serial == thread_pool == interpreter_pool

Verification wall-clock time: ~5s (clone ~1s, compile <1s, lab run ~2s, tests <1s)

JSON, CSV, and RESULTS counts agree: yes (100 rows)
RESULTS.md generated from rows: yes

No interpreter or executor left running: confirmed – all executors use context managers, all direct interpreters closed in finally.

No prohibited paths/tokens/metadata in committed text artifacts: confirmed – scanned README.md, RESULTS.md, cases.json, results_rows.json, results_rows.csv, hn_comments_sanitized.json, hn_thread_evidence.md, VERIFY.md.

HN evidence: dead/flagged entries removed.

Failures: 0

---
This VERIFY documents commit d2c713d164e92f502a291ae7126ba9bda4e024df. A later documentation commit adding this VERIFY.md file was not itself fresh-clone verified.
