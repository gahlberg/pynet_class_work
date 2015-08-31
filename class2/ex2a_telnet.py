#!/usr/bin/env python

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def send_command(remote_conn, cmd):
    '''
    Initiate the Telnet Session
    '''
    cmd = cmd.rstrip()
    remote_conn.write(cmd + '\n')
    time.sleep(1)
    return remote_conn.read_very_eager()

def login(remote_conn, username, password):
    '''
    Login to pynet-rtr1
    '''
    output = remote_conn.read_until("sername:", TELNET_TIMEOUT)
    remote_conn.write(username + '\n')
    output += remote_conn.read_until("ssword:", TELNET_TIMEOUT)
    remote_conn.write(password + '\n')
    return output

def no_more(remote_conn, paging_cmd='terminal length 0'):
    '''
    No paging of Output
    '''
    return send_command(remote_conn, paging_cmd)

def telnet_connect(ip_addr):
    '''
    Establish the Telnet Connection
    '''
    try:
        return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
    except socket.timeout:
        sys.exit("Connection timed-out")


def main():
    '''
    Connect to pynet-rtr1, login, and issue 'show ip int brief'
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()

    remote_conn = telnet_connect(ip_addr)
    output = login(remote_conn, username, password)

    time.sleep(1)
    remote_conn.read_very_eager()
    no_more(remote_conn)

    output = send_command(remote_conn, 'show ip int brief')

    print "\n\n"
    print output
    print "\n\n"

    remote_conn.close()

if __name__ == "__main__":
    main()
