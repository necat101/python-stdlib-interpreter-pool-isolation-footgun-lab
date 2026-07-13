# RESULTS

Python: 3.12.3
Implementation: cpython
Platform: linux
supports_isolated_interpreters: missing
InterpreterPoolExecutor available: False
concurrent.interpreters available: False

Cases: 20
Methods: 5
Rows: 100

Classifications:
- context_only: 20
- local_observation: 1
- not_applicable: 41
- pass: 15
- version_skip: 23

Thread-pool observations: 11 pass, 1 local_observation
Interpreter-pool roundtrips: version_skip (API unavailable in Python 3.12)
Direct interpreter lifecycle: version_skip
Mutable copy boundary: thread shares mutable input (expected)
State isolation: thread sees main module state
Exception preservation: ValueError preserved via ThreadPoolExecutor
Initializer: tag visible in worker thread
Queue: version_skip
Preprocessing equality: serial == thread_pool

No failures. Total runtime <1s.
