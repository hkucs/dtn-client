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


def send_file(addr, port, filename, buffer_len):
    import socket,os
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr, port))
    f = open(filename, "rb")
    basename = os.path.basename(filename)
    s.send(basename)

    while True:
        chunk = f.read(buffer_len)
        if not chunk:
            break
        s.sendall(chunk)
    s.close()
    f.close()

def create_request(start_time, end_time, size, source, destination, t, utility):
    import json
    cmd = {'start_time': start_time, 'end_time': end_time, 'size': size, 'source': source, 'destination': destination, 'type': t, 'utility': str(utility)}
    cmd_json = json.dumps(cmd)
    return cmd_json
