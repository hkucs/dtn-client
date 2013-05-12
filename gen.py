#!/usr/bin/env python

import time
import sys
import os
import random

#INTV=10
NUM_HOSTS=10
HOSTS=['10.6.1.101', '10.6.1.102', '10.6.1.103', '10.6.1.104', '10.6.1.105', '10.6.1.106', '10.6.1.107', '10.6.1.108', '10.6.1.109', '10.6.1.110']
DELAY=14
DL_MR=25
DL_NB=10
PR_MR='1.0'
PR_NB='2.0'

def genMR(INTV):
    size = random.randint(10,20)
    return '%d %s %s %d %d %d %s\n' % (INTV, HOSTS[random.randint(0,NUM_HOSTS-1)], HOSTS[random.randint(0,NUM_HOSTS-1)], size, DELAY, DELAY+size*DL_MR, PR_MR)

def genNB(INTV):
    size = random.randint(1,4)
    return '%d %s %s %d %d %d %s\n' % (INTV, HOSTS[random.randint(0,NUM_HOSTS-1)], HOSTS[random.randint(0,NUM_HOSTS-1)], size, DELAY, DELAY+size*DL_NB, PR_NB)

def gen_req_file(filename):
    # 10min mini test
    #filename = "t600"
    try:

        f = open(filename, "w")
        # generate MR jobs
        req_mr = []
        for x in range(600):
            r = genMR(0)
            req_mr.append(r)

        for x in range(300):
            r = genMR(1)
            req_mr.append(r)

        # generate NB jobs
        req_nb = []
        for x in range(600):
            r = genNB(0)
            req_nb.append(r)

        for x in range(300):
            r = genNB(1)
            req_nb.append(r)

        # shuffle
        req = req_mr + req_nb
        random.shuffle(req)

        for x in req:
            f.write(x)

    except IOError:
        print 'Error opening file %s' % filename

    finally:
        f.close()


if __name__ == '__main__':
    gen_req_file('t600-0-5')
