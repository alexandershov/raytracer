import functools
import multiprocessing
import time
from typing import List


def timed(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        started_at = time.time()
        result = fn(*args, **kwargs)
        duration = time.time() - started_at
        print(f"{fn.__name__} took {duration:.3f}")
        return result

    return inner


def parallel(process_chunk, args, num_processes):
    with multiprocessing.Pool(processes=num_processes) as pool:
        chunks = _get_chunks(args, num_processes)
        return _flatten(pool.map(process_chunk, chunks))


def _flatten(seq_of_seq: List[list]) -> list:
    return [item for seq in seq_of_seq for item in seq]


def _get_chunks(seq: list, n: int) -> List[list]:
    chunks = []
    for i in range(n):
        chunks.append(seq[i::n])
    return chunks
