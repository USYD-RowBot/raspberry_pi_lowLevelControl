from gpiozero import LED
import navio.util
import navio.adc
from time import sleep
led = LED(17)
power=LED(18)
navio.util.check_apm()
adc=navio.adc.ADC()
while True:
    if (adc.read(2)/100<11.8):
        led.on()
        sleep(0.1)
        led.off()
        sleep(0.1)
        power.off()
    else:
        power.on();
        led.off()
