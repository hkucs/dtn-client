#!/usr/bin/env python

from config import *

def b(x):
    if PY3:
        return bytes(x, 'ascii')
    return x

def create_file(filename):
    if os.path.isfile(filename):
        return
    f = open(filename, 'wb')
    chunk_len = 65536
    chunk = b('x' * chunk_len)
    total = 0
    timer = RepeatedTimer(1, lambda: self.print_percent(total, BIGFILE_SIZE))
    timer.start()
    try:
        while 1:
            f.write(chunk)
            total += chunk_len
            if total >= BIGFILE_SIZE:
                break
    finally:
        f.close()
        timer.stop()

def safe_remove(file):
    try:
        os.remove(file)
    except OSError:
        pass

def add_job_chunk(job_id, chunk_id):
    if (job_id, chunk_id) not in cache:
        cache[(job_id, chunk_id)] = 1
