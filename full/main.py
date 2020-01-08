from machine import I2C, Pin, ADC, UART
import time, utime
import network
import _thread
import server

from neopixel import NeoPixel

print('Welcome from IDA Horsens and IDA IT Gruppen Oestjylland')

def do_connect():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('IDA', 'IDAIDAIDA')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    from ntptime import settime
    settime()

def do_lightOn():
    pin = Pin(14, Pin.OUT)
    np = NeoPixel(pin, 7)
    for j in range(np.n):
        np[j] = (255, 255, 255)
    np.write()

def do_lightOff():
    pin = Pin(14, Pin.OUT)
    np = NeoPixel(pin, 7)
    for j in range(np.n):
        np[j] = (0, 0, 0)
    np.write()

do_connect()

while not wlan.isconnected():
    pass

server.start_service(do_lightOn, do_lightOff)
