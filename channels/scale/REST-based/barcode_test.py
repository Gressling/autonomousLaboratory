#!/usr/bin/env python
import os
import sys
import time

import zbar

# create a Processor
proc = zbar.Processor()


def init():
    # Set video device
    video_device = '/dev/video0'
    # Camera set fixed focus
    #os.system('v4l2-ctl -d %s --set-ctrl=focus_auto=0' % video_device)
    #os.system('v4l2-ctl -d %s --set-ctrl=focus_absolute=50' % video_device)

    ## ZBAR init
    proc.parse_config('enable')
    proc.init(video_device)
    proc.visible = True # enable preview
    print 'Barcode scanner initialized.'


if __name__ == '__main__':
    try:
        init()
        while True:
            proc.process_one() # blocking call

            if len(proc.results) > 1:
                print 'More than one barcode scanned!' \
                      ' Please put only one barcode in front of the camera.'
            elif len(proc.results) == 1:
                for symbol in proc.results:
                    print (symbol.type, symbol.data)
            else:
                print 'No barcode found, please empty the scale!'
    except KeyboardInterrupt:
        cleanupAndExit()
