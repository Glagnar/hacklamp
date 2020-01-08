from machine import I2C, Pin, ADC, UART
import time, utime

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


# Pin number 14 with 7 LED's
pin = Pin(14, Pin.OUT)
np = NeoPixel(pin, 7)

# Do lightDemo in 1000 ms
lightDemo(np, 1000)