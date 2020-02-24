#!/usr/bin/env python3

import time
import pigpio
from MotorDriver import L298N

# default vals
FREQ = 250 # turret: 250, on arduino was 244. ~50 is awesome, the lower the Hz, the lower the min PWM needed for motor to start moving
RANGE = 800



class Mover:
    """ combines driver, params, and maybe transformation logic """
    def __init__(self, params, driver):
        self.__driver = driver
        self.__params = params
        driver.setup(params["output"]["freq"], params["output"]["range"])
    def move(self, isBackward, pwmDuty):
        #self.__params["proc"](isBackward, pwmDuty)
        self.__driver.move(isBackward, pwmDuty)



def simple_test(mover):
    for i in range(RANGE+1):
        mover.move(False, i)
        time.sleep(0.005)
    time.sleep(1)
    for i in range(RANGE+1):
        mover.move(True, i)
        time.sleep(0.005)
    time.sleep(1)
    for i in range(RANGE, -1, -1):
        mover.move(True, i)
        time.sleep(0.002)




# data defining axis params: both input (e.g. joystick) and output (motor)
# note: contains no longer used garbage.
genVirtualInputDef = {
    "deadzone": 0, # deadzone radius; joystick: 80
    "center": 512, # joystick: H:508, V:523
    "min": 0,
    "max": 1023,
}
axisVirtualH = {
    "input": genVirtualInputDef,
    "output": {
        "min": 37, # window wiper motor @244Hz: 12/255, ~ 37/800
        "max": RANGE,
        "range": RANGE,
        "freq": FREQ,
    },
    "proc": None, # joystick: 0-1 range squared
}
axisVirtualV = {
    "input": genVirtualInputDef,
    "output": {
        "min": 44, # window wiper motor @244Hz: 14/255, ~ 44/800
        "max": RANGE,
        "range": RANGE,
        "freq": FREQ,
    },
}

pi = pigpio.pi()
if pi.connected:
    motor1 = L298N(pi, {"En": 24, "In0": 17, "In1": 18})
    mover1 = Mover(axisVirtualH, motor1)
    motor2 = L298N(pi, {"En": 23, "In0": 27, "In1": 22})
    mover2 = Mover(axisVirtualV, motor2)
    mover2.move(False, 800)
    simple_test(mover1)
    mover2.move(False, 0)

pi.stop()

