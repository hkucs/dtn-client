#!/usr/bin/env python

import socket,os,sys,json,shutil,datetime,time
import utils
from config import *

def request(source, destination, size=4, delay=30, deadline=90, utility=1.0):
    # number of chunks
    chunk_n = size
    # message
    msg_type = 'request'
    ts_delay = datetime.timedelta(seconds=delay)
    ts_deadline = datetime.timedelta(seconds=deadline)
    ts_now = datetime.datetime.now()

    ts_start = ts_now + ts_delay
    ts_end = ts_now + ts_deadline

    ts_start_out = ts_start.strftime("%Y-%m-%d %H:%M:%S")
    ts_end_out = ts_end.strftime("%Y-%m-%d %H:%M:%S")

    cmd_json = utils.create_request(ts_start_out, ts_end_out, str(size), str(source), str(destination), msg_type, utility)

    print cmd_json

    cmd_json = cmd_json + '\n'

    # create socket
    s = socket.socket()
    s.settimeout(2)
    s.connect(('147.8.178.128', 8088))
    s.sendall(cmd_json)
    s.sendall('\n')

    # waiting for confirmation
    recv_job_id = s.recv(BUFFER_LEN)
    s.close()
    print 'Received job_id: %s. Size: %s' % (recv_job_id, len(recv_job_id))
    recv_job_id = recv_job_id.strip()
    if recv_job_id != '-1':
        job_id = str(recv_job_id).zfill(8)

        # creating dummy chunks
        srcfile = '/data/block'
        assert os.path.isabs(srcfile)
        for x in range(0,chunk_n):
            dstfile = '/data/%s_%s' % (job_id, str(x).zfill(4))
            shutil.copy(srcfile, dstfile)

        return True

    return False

if __name__ == '__main__':

    #print request('10.6.1.101', '10.6.1.102', 4, 10, 110, 1.0)
    #time.sleep(10)
    print request('10.6.1.101', '10.6.1.102', 1, 10, 35, 1.0)
    #print request('10.6.1.102', '10.6.1.103', 3, 33, 39, 1.0)
    #print request('10.6.1.103', '10.6.1.104', 8, 35, 50, 1.0)






'''
def old_main():

    # create json message
    ts_now = datetime.datetime.now()
    ts_60 = datetime.timedelta(seconds=60)
    ts_120 = datetime.timedelta(seconds=120)
    ts_start = ts_now + ts_60
    ts_end = ts_now + ts_120
    ts_start_out = ts_start.strftime("%Y-%m-%d %H:%M:%S")
    ts_end_out = ts_end.strftime("%Y-%m-%d %H:%M:%S")
    cmd_json = utils.create_request(str(ts_start_out), str(ts_end_out), '4', '10.6.1.101', '10.6.1.102', 'request')
    chunk_n= 4 # for convenience
    #cmd_json = 'Hello DTM.'
    print cmd_json
    cmd_json = cmd_json + '\n'

    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(('147.8.178.128', 8088))
    #s.connect(('127.0.0.1', 8088))
    s.sendall(cmd_json)
    s.sendall('\n')

    # wait for confirmation
    recv_job_id = s.recv(BUFFER_LEN)
    #decoded_recv_json = json.loads(recv_json)
    print 'Received job_id: %s. Size: %s' % (recv_job_id, len(recv_job_id))
    recv_job_id = recv_job_id.strip()
    job_id = str(recv_job_id).zfill(8)
    #if 'accept_or_not' in decoded_recv_json:
        #job_id = str(decoded_recv_json.get('job_id')).zfill(8)


    # close connection
    s.close()

    # create chunk files
    srcfile = '/data/block'
    assert os.path.isabs(srcfile)
    for x in range(0,chunk_n):
        dstfile = '/data/%s_%s' % (job_id, str(x).zfill(4))
        shutil.copy(srcfile, dstfile)
'''
