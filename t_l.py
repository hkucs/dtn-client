import json,socket
from config import *

if __name__ == '__main__':
    job_id = '12345678'
    chunk_id = '0002'
    next_hop = '10.6.1.103'

    cmd = {'job_id': job_id, 'chunk_id': chunk_id, 'next_hop': next_hop}
    cmd_json = json.dumps(cmd)
    client = socket.socket()
    client.connect(('10.6.1.101', int(GATEWAY_CMD_PORT)))
    client.send(cmd_json)


