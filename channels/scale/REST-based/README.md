# Scale

Module integrates Raspberry Pi, webcamera with adjustable focus and
HX711 weight sensor. The module weighs a object placed on the sensor,
webcamera scannes a barcode and sends the weight and decoded barcode
to the remote server.

## Installation

This module relies on standard Python 2.7 installation,
[ZBar](http://zbar.sourceforge.net/) library for scannig barcodes,
`requests` python library for HTTP requests and
[HX711py](https://github.com/tatobari/hx711py) library for
interfaceing with the weighing sensor.

For connecting the hardware and using the device, go [HERE](doc/module1.md)

### Install ZBar

Install ZBAR module for pyhton with `apt`:
```
$ sudo apt install python-zbar
```

### Install requests

`requests` should come with the default python installation, if not
install it with `pip`:
```
$ pip install requests
```

### Install HX711py

HX711py library is a submodule of this repo. Either clone this repo with
`--recursive` flag or use the following `git` commands afterwards:
```
$ git submodule init
$ git submodule update
```
If you get a warning from perl:
```
perl: warning: Setting locale failed.
```
Then you need to generate the missing locales (For me it was en_US.UTF-8):
```
$ sudo locale-gen en_US.UTF-8
```
and select newly generated locale(s):
```
$ sudo dpkg-reconfigure locales
```

## Running the module
Position yourself in the `git` repository.
The module is ran simply by issuing the command:
```
$ PYTHONPATH=$PYTHONPATH:./hx711py ./module1.py
```
`hx711py` could be put into the global PYTHONPATH.
