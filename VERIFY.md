# VERIFY

Repository: https://github.com/necat101/python-stdlib-interpreter-pool-isolation-footgun-lab

Verified implementation commit: 2b55e0eff11b93e724df7d6869c7a7164b1946c0

Clone command:
```
git clone https://github.com/necat101/python-stdlib-interpreter-pool-isolation-footgun-lab.git
cd python-stdlib-interpreter-pool-isolation-footgun-lab
git checkout 2b55e0eff11b93e724df7d6869c7a7164b1946c0
```

Python executable: /usr/bin/python3
Python version: 3.12.3
Implementation: cpython
Platform: linux

API availability:
- supports_isolated_interpreters: missing
- InterpreterPoolExecutor available: False
- concurrent.interpreters available: False

Validation commands:
```
python3 -m py_compile run_lab.py worker_tasks.py test_lab.py
# exit code: 0

python3 run_lab.py
# exit code: 0
# Wrote 100 rows

python3 -m unittest -v
# exit code: 0
# Ran 11 tests – OK
```

Unittest count: 11
Cases: 20
Methods: 5
Rows: 100

Classification counts:
- pass: 15
- local_observation: 1
- version_skip: 23
- context_only: 20
- not_applicable: 41
- fail: 0

Verification wall-clock time: ~10s (clone ~1s, compile <1s, lab run ~1s, tests <1s)

JSON, CSV, and RESULTS counts agree: yes (100 rows)

No interpreter or executor left running: confirmed – all executors use context managers, direct interpreter API unavailable so no interpreters created.

No prohibited paths/tokens/metadata in committed text artifacts: confirmed.

Honest skips: InterpreterPoolExecutor and concurrent.interpreters are unavailable in Python 3.12 – all interpreter-dependent rows correctly marked version_skip.

Failures: 0

---
This VERIFY documents commit 2b55e0eff11b93e724df7d6869c7a7164b1946c0. A later documentation commit adding this VERIFY.md file was not itself fresh-clone verified.
