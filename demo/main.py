from machine import I2C, Pin, ADC, UART
import time
import utime
import network
import _thread
import server

import ssd1306

from neopixel import NeoPixel

print('Welcome from IDA Horsens and IDA IT Gruppen Oestjylland')

def lightDemo(np, pause):
    time.sleep_ms(pause)

    while True:
        n = np.n

        # cycle
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 0)
            np[i % n] = (255, 255, 255)
            np.write()
            time.sleep_ms(25)

        # bounce
        for i in range(4 * n):
            for j in range(n):
                np[j] = (0, 0, 128)
            if (i // n) % 2 == 0:
                np[i % n] = (0, 0, 0)
            else:
                np[n - 1 - (i % n)] = (0, 0, 0)
            np.write()
            time.sleep_ms(60)

        # fade in/out
        for i in range(0, 4 * 256, 8):
            for j in range(n):
                if (i // 256) % 2 == 0:
                    val = i & 0xff
                else:
                    val = 255 - (i & 0xff)
                np[j] = (val, 0, 0)
            np.write()

        # clear
        for i in range(n):
            np[i] = (0, 0, 0)
        np.write()

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

def do_light_demo():
    pin = Pin(14, Pin.OUT)
    np = NeoPixel(pin, 12)

    pin2 = Pin(15, Pin.OUT)
    np2 = NeoPixel(pin2, 7)

    pin3 = Pin(27, Pin.OUT)
    np3 = NeoPixel(pin3, 33)

    _thread.start_new_thread(lightDemo, (np, 0))
    _thread.start_new_thread(lightDemo, (np2, 0))
    _thread.start_new_thread(lightDemo, (np3, 0))

def update_display(display):
    while True:
        display.fill(0)
        display.text("IDA HORSENS", 0, 0)

        if not wlan.isconnected():
            display.text("Ingen WiFi", 0, 10)
        else:
            display.text(wlan.ifconfig()[0], 0, 10)
        display.show()

        display.text(str(utime.localtime()[3] + 1) + ":" + str(utime.localtime()[4]) + ":" + str(utime.localtime()[5]), 0, 20)

        time.sleep_ms(5000)


def do_display():
    # Setup Display on default pins
    i2c = I2C(-1, Pin(22), Pin(23))

    global display
    display = ssd1306.SSD1306_I2C(128, 64, i2c)
    _thread.start_new_thread(update_display, (display, ))

def do_relay():
    while True:
        do_relayOn()
        time.sleep(10000)
        do_relayOff()
        time.sleep(10000)

def do_relayOn():
    pinOn = Pin(13, Pin.OUT)
    pinOn.value(1)
    time.sleep_ms(50)
    pinOn.value(0)

def do_relayOff():
    pinOff = Pin(12, Pin.OUT)
    pinOff.value(1)
    time.sleep_ms(50)
    pinOff.value(0)


do_display()
do_connect()
_thread.start_new_thread(do_relay, ())

while not wlan.isconnected():
    pass
server.start_service(do_relayOn, do_relayOff)
