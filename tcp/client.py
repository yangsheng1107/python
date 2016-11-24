#!/usr/bin/python

import os
import subprocess
import socket
import sys
import errno
import time

def tcp_client_test(timeout=5, host=None, port=None, message=None):
    check = False
    time_now = 0

    if host==None or port==None or message==None:
        return check

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.setblocking(0)
        s.settimeout(5)
    except socket.error as msg:
        if s:
            s.close()
        print "Could not open socket:%s" % msg
        return check

    while time_now < timeout:
        try:
            num = s.send(message)
            print "send \"%s\" in %d byte " % (message, num)
            break

        except socket.timeout:
            print 'accept ' + host + ':' + str(port) + ' time out...'
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
    if len(sys.argv) != 4:
        print " Using : %s <ip> <port> <message>" % sys.argv[0]
        sys.exit(1) 

    tcp_client_test(5,sys.argv[1], sys.argv[2], sys.argv[3])