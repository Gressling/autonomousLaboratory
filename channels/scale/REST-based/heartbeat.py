#!/usr/bin/python

import socket
import requests
import sys
import json
import threading

def start(channel):
    heartbeat(channel)
    threading.Timer(2, start, [channel]).start()


def heartbeat(cognitive_channel):
    ip = socket.gethostbyname(socket.gethostname())
    payload = {'meta': {'id': cognitive_channel, 'ip': ip},
               'data': {}}
    try:
        return requests.post("http://stem.xxx.net/api/iot",
                             json=payload)
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    start(sys.argv[1])
