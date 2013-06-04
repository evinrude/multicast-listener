#!/usr/bin/env python
# Python 2 and 3 compatible

import socket
import struct
import sys
import signal
import getopt


class Main:

    G_SOCKET = ""
    G_MREQ = ""
    
    # Control-C routine - be a good neighbor and leave the multicast group
    def leavegroup(self, signal, frame):
        print("Leaving Group")
        self.G_SOCKET.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, self.G_MREQ)
        sys.exit()


    def doit(self, multicast_group, multicast_port):
        # Setup the initial socket
        self.G_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # Allow reuse
        self.G_SOCKET.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind
        self.G_SOCKET.bind(multicast_port)

        # Let the router/switch know that we want to recieve traffic
        group = socket.inet_aton(multicast_group)
        self.G_MREQ = struct.pack('4sL', group, socket.INADDR_ANY)
        self.G_SOCKET.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.G_MREQ)

        # Endless loop of traffic
        while True:
            print("\nwaiting to receive message")
            data, address = self.G_SOCKET.recvfrom(1024)
            print("received %s bytes from %s" % (len(data), address))
            print(data)


# Entry Point
if __name__ == "__main__":
    opts = getopt.getopt(sys.argv[1:],"g:p:","")
    for option in opts[0]:
        if option[0] == '-g':
            multicast_group = option[1]
        if option[0] == '-p':
            multicast_port = ('',int(option[1]))

    # Check for arguments
    try:
        if not multicast_group or not multicast_port:
           print("You should not be seeing this")
    except:
        print("\nUsage: %s -g XXX.XXX.XXX.XXX -p XXXXX\n" % sys.argv[0])
        sys.exit()


    # Do it
    try:
        main = Main()
        signal.signal(signal.SIGINT, main.leavegroup)
        main.doit(multicast_group, multicast_port)
    except Exception as exc:
        print(exc)


