#!/usr/bin/python

import os
import subprocess
import socket
import sys
import errno
import time

def tcp_server_test(timeout=5, host=None, port=None):
    check = False
    time_now = 0
    conn = None

    if host==None or port==None:
        return check

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, int(port)))
        s.listen(1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(0)
        s.settimeout(5)
    except socket.error as msg:
        if s:
            s.close()
        print "Could not open socket:%s" % msg
        return check

    while time_now < timeout:
        try:
            if not conn:
                conn, addr = s.accept()

            data = conn.recv(1024)
            print 'Recv from ' + addr[0] + ':' + str(addr[1])

            if data is None:
                time.sleep(1)
                time_now += 1
            else:
                print data
                break

        except socket.timeout:
            print 'accept ' + host + ':' + str(port) + ' time out...'
            time.sleep(1)
            time_now += 1
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                sleep(1)
                continue
            else:
                print e
                break

    if conn:
        conn.close()
    if s:
        s.close()

    return check

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print " Using : %s <ip> <port>" % sys.argv[0]
        sys.exit(1)
    
    tcp_server_test(5, sys.argv[1], sys.argv[2])