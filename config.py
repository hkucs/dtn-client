import sys

CONTROLLER_PORT='8088'
GATEWAY_CMD_PORT='16001'
GATEWAY_DAT_PORT='16002'

BUFFER_LEN = 1024
HEADER_LEN = 13
BIGFILE_SIZE = 10000000 # 10m

PY3 = sys.version_info >= (3,)

# buffer management per gateway
cache = {}
