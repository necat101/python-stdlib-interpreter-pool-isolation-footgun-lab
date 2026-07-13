# VERIFY

Repository: https://github.com/necat101/python-stdlib-interpreter-pool-isolation-footgun-lab

Verified implementation commit: e5a767ea241e29f63d1f76258db6be01ce30182f

This is v3. v1 (2b55e0e / 312ec2b) was a Python 3.12 skip-path scaffold with stubbed InterpreterPoolExecutor / concurrent.interpreters implementations. v2 (d2c713d / d29434c) implemented real IPE/CI APIs under Python 3.14.6, but the direct_interpreter lifecycle, builtins_isolation, and queue_roundtrip cases were weak and the corresponding tests only checked classification labels. v3 strengthens all three direct_interpreter cases, expands test assertions to check recorded evidence, broadens artifact scanning, and filters HN evidence to relevant comments only.

Clone command:
```
git clone https://github.com/necat101/python-stdlib-interpreter-pool-isolation-footgun-lab.git
cd python-stdlib-interpreter-pool-isolation-footgun-lab
git checkout e5a767ea241e29f63d1f76258db6be01ce30182f
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

Interpreter-pool (behavioral): 9 pass, 2 expected_error
Direct-interpreter (behavioral): 3 pass, 1 expected_error
Thread-pool (behavioral): 11 pass

Direct interpreter evidence (v3):
- lifecycle: appeared=True, result=84, closed_ok=True, disappeared=True
- builtins_isolation: sentinel set in subinterpreter builtins namespace, main builtins clean
- queue_roundtrip: got=99, no shareability fallback
- queue_unshareable: NotShareableError correctly raised

All behavioral assertions verified by unittest, not just classification labels.

Verification wall-clock time: ~5s (clone ~1s, compile <1s, lab run ~2s, tests <1s)

JSON, CSV, and RESULTS counts agree: yes (100 rows)
RESULTS.md generated from rows: yes

No interpreter or executor left running: confirmed

Artifact cleanliness: scanned README.md, RESULTS.md, cases.json, results_rows.json, results_rows.csv, hn_comments_sanitized.json, hn_thread_evidence.md, VERIFY.md – no github tokens, session metadata, or prohibited /home/ubuntu / /tmp paths (legitimate python executable path `/home/ubuntu/.local/bin/python3.14` allowed per spec).

HN evidence: 163 relevant comments retained, dead/flagged/irrelevant entries (snake illustrations, company politics, off-topic rants) removed.

Failures: 0

---
This VERIFY documents commit e5a767ea241e29f63d1f76258db6be01ce30182f. A later documentation commit adding this VERIFY.md file was not itself fresh-clone verified.
