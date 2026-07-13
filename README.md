# python-stdlib-interpreter-pool-isolation-footgun-lab

Python 3.14 `concurrent.futures.InterpreterPoolExecutor` / `concurrent.interpreters` isolation semantics – stdlib-only correctness lab.

This repository tests interpreter isolation, serialization boundaries, mutable state, initializer behavior, exception propagation, cross-interpreter queues, and distinguishes a narrow deterministic preprocessing test from broad ML performance claims.

**Python tested:** 3.14.6 (CPython, Linux)  
`InterpreterPoolExecutor` available: **Yes**  
`concurrent.interpreters` available: **Yes**

## Results summary

- Cases: 20
- Methods: 5 (`inspect_api`, `thread_pool_comparison`, `interpreter_pool_operation`, `direct_interpreter_operation`, `hn_context_observation`)
- Rows: 100
- Classifications: pass 32, expected_error 3, local_observation 2, context_only 20, not_applicable 43, fail 0
- Thread-pool: 11 pass
- Interpreter-pool: 9 pass, 2 expected_error (lock serialization rejection, initializer failure)
- Direct-interpreter: 3 pass, 1 expected_error (queue unshareable object)
- Preprocessing token-count: serial == thread_pool == interpreter_pool

See `RESULTS.md` for full counts.

## What this lab does NOT prove

- Free-threaded Python is faster for every workload
- Subinterpreters are faster than processes or ordinary threads
- Python extension modules are subinterpreter-safe
- An interpreter pool makes NumPy, PyTorch, pandas, or scikit-learn compatible
- Isolated interpreters are a security sandbox
- A tiny token-count task predicts ML training performance
- Matching local results prove race freedom

## Hacker News thread access

Thread: https://news.ycombinator.com/item?id=44003445  
Article: https://labs.quansight.org/blog/free-threaded-one-year-recap  
PEP 703 (free-threaded / no-GIL): https://peps.python.org/pep-0703/  
PEP 734 (subinterpreters / InterpreterPoolExecutor): https://peps.python.org/pep-0734/

Tool used: Hacker News API CLI  
Command: `python3 ./hackernews get-item --id 44003445`  
Skill path: `openclaw.extensions.hackernews`

Evidence was captured before the sentiment summary was prepared. Dead/flagged entries excluded. See `hn_comments_sanitized.json` and `hn_thread_evidence.md`.

## The linked article vs HN commenters vs this lab

**Linked article (Quansight, "The first year of free-threaded Python"):** recounts CPython's free-threaded (no-GIL) build one year after PEP 703, ecosystem enablement progress, and performance observations.

**HN commenters expressed (thread 44003445, paraphrased, see evidence files):**

- Some commenters were excited about using multiple CPU cores without multiprocessing workarounds – avoiding process startup costs, pickling/serialization overhead for sharing data between processes, and fork-related limitations.
- Others emphasized that shared-state threading can expose races and bugs that the GIL previously made harder to hit – race conditions become easier to trigger when threads truly run in parallel.
- Single-threaded slowdown came up repeatedly – removing the GIL can make single-threaded code slower, which is a tradeoff for users who don't need parallelism.
- Process startup and serialization costs came up as a motivation for threads – multiprocessing requires pickling objects back and forth, shared memory involves explicit setup, fork can have issues with threads.
- Shared mutable state is both useful and dangerous – explicit sharing is not a huge burden compared to debugging accidental sharing bugs; people disagree about whether threads or multiprocessing is the right default.
- Compiled extension modules need auditing – the library ecosystem may not be ready for free-threaded Python; C extensions that relied on GIL semantics need review.
- NumPy, SciPy, pandas, scikit-learn, PyTorch, and the broader PyData ecosystem came up as central to the discussion – performance-sensitive Python code often delegates to C extensions like NumPy; one commenter reported trying PyTorch with free-threaded Python and observing higher CPU usage for less work.
- Some commenters preferred free-threading over subinterpreters – using real shared-memory threads in one interpreter.
- Others considered isolated interpreters or processes easier to reason about – separate state reduces accidental sharing bugs.
- Support for free-threading does not automatically imply support for subinterpreters – these are different concurrency models with different isolation guarantees.
- Anecdotal performance results should not be treated as universal benchmarks – a commenter's PyTorch timing or a local timing report does not establish universal performance characteristics.
- A commenter's claim about NumPy and subinterpreters, if present in the thread, must be attributed as a commenter's position rather than presented as an official NumPy policy unless separately sourced.

**This repository tests (separate from both the article and HN comments):**

Python 3.14 `concurrent.futures.InterpreterPoolExecutor` and the lower-level `concurrent.interpreters` module – interpreter isolation, serialization boundaries, mutable state, initializer behavior, exception propagation, cross-interpreter queues.

This is about **PEP 734 subinterpreters / InterpreterPoolExecutor**, NOT about PEP 703 free-threaded Python (no-GIL). Free-threading and isolated subinterpreters are different concurrency models:

- Free-threaded Python (PEP 703): removes the GIL, threads in one interpreter share all state, need locking for shared mutable data.
- Subinterpreters / InterpreterPoolExecutor (PEP 734): each worker runs in an isolated interpreter with separate module state, explicit serialization boundaries – more like processes than threads.

Subinterpreters still impose explicit state and serialization boundaries. Process overhead, copying, shared state, and maintainability represent different tradeoffs. Anecdotal PyTorch or local timing reports do not establish universal performance. This lab tests stdlib semantics, not realistic model training.

## Run

```sh
python3 -m py_compile run_lab.py worker_tasks.py test_lab.py
python3 run_lab.py
python3 -m unittest -v
```

Lab runtime: <5s. Test suite: <1s.
