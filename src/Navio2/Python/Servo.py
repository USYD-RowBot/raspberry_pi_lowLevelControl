#!/usr/bin/env python
import sys
import time

import navio.pwm
import navio.util

navio.util.check_apm()

PWM_OUTPUT = 0
SERVO_MIN = 1.200 #ms
SERVO_MAX = 1.800 #ms

with navio.pwm.PWM(PWM_OUTPUT) as pwm:
    pwm.set_period(20)
    pwm.disable()
    time.sleep(10)
    pwm.enable()
    pwm.set_duty_cycle(1.500)
    
    print("Trying intialisation with 1.5")
    time.sleep(10)

    print("Ending init")

    print("Run")
    pwm.set_duty_cycle(SERVO_MAX)
    time.sleep(10)
    print("Done")
    
    #print("Turning on")
    #time.sleep(5)
    #pwm.set_duty_cycle(1.700) # Give it a kick at first
    #print("Giving it a boost")
    #time.sleep(5)
    #pwm.set_duty_cycle(1.5)
    #print("Print starting initialisation, set 1500")
    #time.sleep(15)
    #print("End of initialisation")

    #pwm.set_duty_cycle(1.700)
    #print("Running, set 1700")
    #time.sleep(10)


    """ print("1.5")
    time.sleep(1)
    pwm.set_duty_cycle(1.600)
    print("1.6")
    time.sleep(1)
    pwm.set_duty_cycle(1.700)
    print("1.7")
    time.sleep(1)
    pwm.set_duty_cycle(1.600)
    print("1.6")
    time.sleep(1)
    pwm.set_duty_cycle(1.500)
    print("1.5")
    time.sleep(2)
    pwm.set_duty_cycle(1.400)
    print("1.4")
    time.sleep(20)
    pwm.set_duty_cycle(1.500)
    time.sleep(5)
    print("ready")
    while (True):
        print("cycle")
        pwm.set_duty_cycle(SERVO_MIN)
        time.sleep(1)
        pwm.set_duty_cycle(SERVO_MAX)
        time.sleep(1)
    """
