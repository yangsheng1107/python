#!/usr/bin/python

import os
import subprocess
import socket
import sys
import errno
import time

def udp_server_test(timeout=5, host=None, port=None):
    check = False
    time_now = 0

    if host==None or port==None:
        return check

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, int(port)))
        s.setblocking(0)
        s.settimeout(5)
    except socket.error as msg:
        if s:
            s.close()
        print "Could not open socket:%s" % msg
        return check

    while time_now < timeout:
        try:
            data, addr = s.recvfrom(1024)
            print 'Recv from ' + addr[0] + ':' + str(addr[1])

            if data is None:
                time.sleep(1)
                time_now += 1
            else:
                print data
                break

        except socket.timeout:
            print 'Recv time out...'
            time.sleep(1)
            time_now += 1
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                time.sleep(1)
                continue
            else:
                print e
                break
    if s:
        s.close()
    return check


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print " Using : %s <ip> <port>" % sys.argv[0]
        sys.exit(1)

    udp_server_test(5, sys.argv[1], sys.argv[2])