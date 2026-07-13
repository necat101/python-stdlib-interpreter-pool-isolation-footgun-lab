"""worker_tasks.py - top-level callables for interpreter-pool lab."""
# global mutable state
worker_counter = 0
worker_tag = None

def simple_add(a, b):
    return a + b

def tuple_transform(x):
    return (x, x * 2, f"v{x}")

def checksum_ints(vals):
    return sum(vals)

def append_one(xs):
    # appends one fixed value, returns snapshot
    out = list(xs)
    out.append(42)
    return tuple(out)

def read_worker_counter():
    global worker_counter
    return worker_counter

def inc_worker_counter():
    global worker_counter
    worker_counter += 1
    return worker_counter

def reset_worker_counter():
    global worker_counter
    worker_counter = 0
    return worker_counter

def read_worker_tag():
    global worker_tag
    return worker_tag

def set_worker_tag(tag):
    global worker_tag
    worker_tag = tag
    return worker_tag

def init_set_tag():
    global worker_tag
    worker_tag = "initialized"
    return None

def init_fail():
    raise RuntimeError("intentional-initializer-error")

def raise_value_error():
    raise ValueError("intentional-interpreter-lab-error")

def token_count(text):
    # lowercase, split whitespace, return sorted mapping
    tokens = text.lower().split()
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return dict(sorted(counts.items()))

def map_token_count(texts):
    return [token_count(t) for t in texts]
