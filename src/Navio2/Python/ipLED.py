import sys

import navio.leds
import time
import navio.util
import navio.adc
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


navio.util.check_apm()

led = navio.leds.Led()
adc=navio.adc.ADC()
# trueIP=trueIP.split(".")
while (True):
    # first check if power is above or below minimum
    while (adc.read(2)/100<11.8):
        led.setColor('Red')
        time.sleep(0.1)
        led.setColor('Black')
        time.sleep(0.1)
    # fetch our IP address
    trueIP = get_ip()
    for i in trueIP:
        try:
            count = int(i)
            for j in range(count):
                led.setColor('Green')
                time.sleep(0.2)
                led.setColor('Black')
                time.sleep(0.2)
            led.setColor('Yellow')
            time.sleep(0.7)
            led.setColor('Black')
            time.sleep(0.7)
        except Exception:
            led.setColor('Red')
            time.sleep(0.7)
            led.setColor('Black')
            time.sleep(0.7)
    led.setColor('Blue')
    time.sleep(0.7)
    led.setColor('Black')
    time.sleep(0.7)
