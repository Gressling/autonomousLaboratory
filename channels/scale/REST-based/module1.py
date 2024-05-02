#!/usr/bin/env python
import os
import sys
import time
import collections

import RPi

import requests
import zbar

import hx711
import heartbeat

REFERENCE_UNIT = 6246.0
HTTP_TIMEOUT = 2
POST_URL = 'http://stem.xxx.net/api/iot'

MINIMUM_TRIGGER_WEIGHT_IN_GRAM = 2 

# create a Processor
proc = zbar.Processor()
hx = hx711.HX711(24, 23)


def get_reference_unit():
    print('\nPlease put a known weight on the scale.')
    c = str()
    c = input('Enter "c" to continue: ')
    print('Weighing known weight...')
    measured_weight = hx.get_weight(60)
    try:
        response = input('Known weight in grams: ')
        known_weight = float(response)
    except ValueError:
        print('Please enter a valid number.')
    return measured_weight/known_weight


def init():
    # Set video device
    video_device = '/dev/video0'
    if len(sys.argv) > 1:
        video_device = sys.argv[1]
    # Camera set fixed focus
    os.system('v4l2-ctl -d %s --set-ctrl=focus_auto=0' % video_device)
    os.system('v4l2-ctl -d %s --set-ctrl=focus_absolute=50' % video_device)

    ## ZBAR init
    proc.parse_config('enable')
    proc.init(video_device, False)
    # proc.visible = True # enable preview
    print('Barcode scanner initialized.')

    ## HX711 init
    #  find zero weight
    print('\n*** Starting device calibration ***')
    print('\nPlease remove any weight from the device.')
    c = str()
    c = input('Enter "c" to continue: ')
    print('Finding zero weight...')
    hx.tare(60)
    #  calibrate the sensor
    hx.set_reference_unit(get_reference_unit())

    #  set reading formats, look in the example of hx711 module
    hx.set_reading_format('LSB', 'MSB')
    print('\n*** Device calibrated ***')

    # wait for the calibration weight to be removed
    print('\nPlease remove the calibration weight.')
    while True:
        if hx.get_weight(5) < 0.3:
            print('Calibration weight removed. \nDevice is ready for use...\n')
            break


def send_to_server(weight, symbol):
    print('Barcode scanned...')
    print('Type: %s, Data: "%s"' % (symbol.type, symbol.data))
    print('Weight: %s g' % weight)
    json_data = {'meta': {'id': 'iot5'}, 'data': {'mg': 0.0, 'QRcode': ''}}
    json_data['data']['mg'] = weight
    json_data['data']['QRcode'] = symbol.data
    try:
        response = requests.post(POST_URL, json=json_data, timeout=HTTP_TIMEOUT)
        print('POST %s to %s' % (json_data, POST_URL))
        print('Server replied:\n%s\n' % response.content)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        print('  ERROR: %s\n' % e)
        print('Please empty the scale!')


def cleanupAndExit():
    print('\nCleanup...')
    proc.visible = False
    RPi.GPIO.cleanup()
    print('Bye!')
    sys.exit()


if __name__ == '__main__':
    try:
        init()
        while True:
            heartbeat.heartbeat('iot5')
            current_weight = hx.get_weight(5)
            if current_weight > MINIMUM_TRIGGER_WEIGHT_IN_GRAM:
                print('Scale loaded, looking for a barcode...')
                proc.process_one(timeout=1)

                if len(proc.results) > 1:
                    print('More than one barcode scanned!' \
                          ' Please put only one barcode in front of the camera.')
                elif len(proc.results) == 1:
                    for symbol in proc.results:
                        # wait for the scale to stabilize
                        weight_buffer = collections.deque([0.0] * 10, maxlen=10)
                        while True:
                            weight_buffer.append(round(hx.get_weight(1), 2))
                            if max(weight_buffer) - min(weight_buffer) < 1:
                                break
                        current_weight = "{0:.1f}".format(sum(weight_buffer)/weight_buffer.maxlen)
                        send_to_server(current_weight, symbol)
                else:
                    print('No barcode found, please empty the scale!')
                # restart the hx711 ADC
                hx.power_down()
                time.sleep(1)
                hx.power_up()
    except KeyboardInterrupt:
        cleanupAndExit()
