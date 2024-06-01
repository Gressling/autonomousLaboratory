import os
import sys
import time
import contextlib

import json
import requests

import cv2
import picamera


WATSON_URL = 'https://gateway-a.watsonplatform.net/visual-recognition/api/v3/classify?api_key=e96c7ba1dfa8bea69dcb01b94f6d214a805ab3b1&version=2016-05-20'
BLUEMIX_URL = 'http://stem.mybluemix.net/api/iot'
USB_CAM_AVAILABLE = os.path.exists('/dev/video0')


@contextlib.contextmanager
def delay_to_one_second(s):
    t1 = time.time()
    yield
    t2 = time.time()
    total_time = t2 - t1
    print s % total_time
    if total_time < 1:
        print '  Sleeping for %s' % (1 - total_time)
        time.sleep(1 - total_time)


def take_picture_every_second():
    if USB_CAM_AVAILABLE:
        usb_camera = cv2.VideoCapture(0)
        while(True):
            s, img = usb_camera.read()
            if s:
                with delay_to_one_second('  USB Camera image sent in: %s sec'):
                    cv2.imwrite('temp.jpg', img)
                    send_image()
    else:
        with picamera.PiCamera() as pi_camera:
            pi_camera.resolution = (640, 480)
	    while(True):
                with delay_to_one_second('  PiCamera image sent in: %s sec'):
                    pi_camera.capture('temp.jpg')
                    send_image()

def send_image():
    with open('temp.jpg', 'rb') as images_file, open('classifier_ID.json', 'rb') as parameters:
        try:
            files = {'images_file': ('temp.jpg', images_file, 'image/jpeg'),
                     'parameters': ('classifier_ID.json', parameters, 'application/json')}
            r = requests.post(WATSON_URL, files=files)
            print 'POST image.jpg to -> ', WATSON_URL
            print r.text
            reply = '{"meta": {"id": "iot1"}, "data": %s}' % r.text
            r = requests.post(BLUEMIX_URL, data=reply, headers={'Content-Type': 'application/json'})
            print 'Sending reply to %s...' % BLUEMIX_URL
            print r.text

        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print '  ERROR: %s\n' % e

if __name__ == '__main__':
    try:
        take_picture_every_second()
    except KeyboardInterrupt:
        print '\nQuitting...'
        exit()
