from abc import ABC, abstractmethod # AbstractBaseClass
import pigpio




class MotorDriver(ABC): # is NOT aware of PWM range
    """ Single motor control, parent class """
    def __init__(self, pi, pins):
        self.__pi = pi
        self.__pins = pins
    def setup(self, freq, range):
        for pin in (self.__pins.values()):
            self.__pi.set_mode(pin, pigpio.OUTPUT)
            self.__pi.set_PWM_frequency(pin, freq)
            self.__pi.set_PWM_range(pin, range)
            self.__pi.set_PWM_dutycycle(pin, 0)
    def pi(self):
        """ convenience to avoid super in subclasses """
        return self.__pi
    def pins(self):
        """ convenience to avoid super in subclasses """
        return self.__pins
    @abstractmethod
    def move(self, isBackward, pwmDuty): pass

class L298N(MotorDriver):
    """ Can use 2 of these per 1 L298 module.
    pins: "En", "In0", "In1" """
    def move(self, isBackward, pwmDuty):
        self.pi().set_PWM_dutycycle(self.pins()["En"], pwmDuty)
        self.pi().write(self.pins()["In0"], 0 if (isBackward or pwmDuty == 0) else 1)
        self.pi().write(self.pins()["In1"], 0 if (not isBackward or pwmDuty == 0) else 1)

class BTS796(MotorDriver):
    """ Pull Enable pins up. No reason to use them, BOTH must be HIGH anyway.
    pins: "PWM1", "PWM2" """
    def move(self, isBackward, pwmDuty):
        self.__pi.set_PWM_dutycycle(pins["PWM1"], pwmDuty if isBackward else 0)
        self.__pi.set_PWM_dutycycle(pins["PWM2"], pwmDuty if not isBackward else 0)


