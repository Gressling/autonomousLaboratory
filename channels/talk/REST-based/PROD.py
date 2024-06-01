#!/usr/bin/python

import requests
import sys, os
import datetime
import time
import json
from pprint import pprint


def talk():

        os.system("rm -r out.json")
        os.system("curl -s -X POST -H \"Content-Type: application/json\" -d \"@isAlive.json\" \"http://gressling.net/api/iot\" >> out.json")
        os.system("cat out.json")
        os.system("echo")
        with open('out.json') as data_file:
            data = json.load(data_file)
        #pprint(data)
        pprint(data)
        pprint('answers' in data)
        if 'answers' in data:
            if len(data["answers"]) > 0 :
                pprint(data["answers"][0]["data"]["text"])

                headers = {'accept': 'audio/wav'}
                str="https://gressling.net/text-to-speech/api/v1/synthesize?text="+data["answers"][0]["data"]["text"]
                print(str)
                r = requests.get(str, auth=('<NAME>', '<API-TOKEN>'), headers=headers)
                with open(sys.path[0] + '/tmp.wav', 'wb') as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
	            os.system("aplay {}/tmp.wav".format(sys.path[0]))


while True:
      try:
        talk()
        time.sleep(0.5)
      except KeyboardInterrupt:
        exit()
      



