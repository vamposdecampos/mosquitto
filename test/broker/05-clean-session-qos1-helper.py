#!/usr/bin/env python

# Test whether a clean session client has a QoS 1 message queued for it.

import inspect, os, sys
# From http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import mosq_test

rc = 1
keepalive = 60
connect_packet = mosq_test.gen_connect("test-helper", keepalive=keepalive)
connack_packet = mosq_test.gen_connack(rc=0)

mid = 128
publish_packet = mosq_test.gen_publish("qos1/clean_session/test", qos=1, mid=mid, payload="clean-session-message")
puback_packet = mosq_test.gen_puback(mid)

sock = mosq_test.do_client_connect(connect_packet, connack_packet)
sock.send(publish_packet)

if mosq_test.expect_packet(sock, "puback", puback_packet):
    rc = 0

sock.close()

exit(rc)

