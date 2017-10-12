from __future__ import division
import time
import threading
import queue
import generic.send_data as send_data
import uuid_defines as my_ids

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

ON = 4095
OFF = 0
#current = 0

#id
LED1 = 1
LED2 = 2
#LED1and2 = 3

LED1_RED = 13
LED1_BLUE = 14
LED1_GREEN = 15

LED2_RED = 10
LED2_BLUE = 11
LED2_GREEN = 12

STEP_SIZE =10

class LedObj():
    def __init__(self):
        self.red = 0
        self.blue = 0
        self.green = 0
        self.going_up = True
        self.intensity = 100
        self.currentIntensity = 100
        self.time = 0
        self.currentRed = 0
        self.currentGreen = 0
        self.currentBlue = 0


class LedControl():

    def __init__(self, sendQueue):
        self.threadLed1 = threading.Thread(target=self.led1Loop)
        self.threadLed1.setDaemon(True)
        self.id_led = 0
        self.lock1 = threading.Lock()
        self.running1 = False
        self.ledBoth = LedObj()
        self.threadLed1.start()
        self.sendToQueue = sendQueue

    def colorScale(self, value):
        calculated = int(ON / 255 * value)
        #print(calculated)
        return calculated

    def brightnessScale(self, value):
        return(int(value * (self.ledBoth.currentIntensity/100)))

    def led1Loop(self):
        while True:
            sleep_time = 0.1
            self.lock1.acquire()
            if self.ledBoth.time > 0:
                #if self.ledBoth.red > 0:
                sleep_time = (self.ledBoth.time/1000)/(100 / STEP_SIZE)

                if self.ledBoth.going_up:
                    if self.ledBoth.currentIntensity > (100-STEP_SIZE):
                        self.ledBoth.going_up = False
                        self.ledBoth.currentIntensity = self.ledBoth.currentIntensity - STEP_SIZE
                    else:
                        self.ledBoth.currentIntensity = self.ledBoth.currentIntensity + STEP_SIZE
                else:
                    if self.ledBoth.currentIntensity < (0+STEP_SIZE):
                        self.ledBoth.going_up = True
                        self.ledBoth.currentIntensity = self.ledBoth.currentIntensity + STEP_SIZE
                    else:
                        self.ledBoth.currentIntensity = self.ledBoth.currentIntensity - STEP_SIZE
            pwm.set_pwm(LED1_RED, 0, self.brightnessScale(self.ledBoth.currentRed))
            pwm.set_pwm(LED1_BLUE, 0, self.brightnessScale(self.ledBoth.currentBlue))
            pwm.set_pwm(LED1_GREEN, 0, self.brightnessScale(self.ledBoth.currentGreen))
            pwm.set_pwm(LED2_RED, 0, self.brightnessScale(self.ledBoth.currentRed))
            pwm.set_pwm(LED2_BLUE, 0, self.brightnessScale(self.ledBoth.currentBlue))
            pwm.set_pwm(LED2_GREEN, 0, self.brightnessScale(self.ledBoth.currentGreen))

            self.lock1.release()
            time.sleep(sleep_time)

    def setLedRed(self, value):
        self.lock1.acquire()
        self.ledBoth.red = value
        self.ledBoth.currentRed = self.colorScale(value)
        self.sendToQueue.put(report)
        self.sendToQueue.put(control)
        self.lock1.release()

    def setLedGreen(self, value):
        self.lock1.acquire()
        self.ledBoth.green = value
        self.ledBoth.currentGreen = self.colorScale(value)
        self.lock1.release()

    def setLedBlue(self, value):
        self.lock1.acquire()
        self.ledBoth.blue = value
        self.ledBoth.currentBlue = self.colorScale(value)
        self.lock1.release()

    def setLedBrightness(self, value):
        self.lock1.acquire()
        self.ledBoth.intensity = value
        self.ledBoth.currentIntensity = value
        self.lock1.release()

    def setLedTime(self, value):
        self.lock1.acquire()
        self.ledBoth.time = value
        if value == 0:
            self.ledBoth.currentRed = self.colorScale(self.ledBoth.red)
            self.ledBoth.currentGreen = self.colorScale(self.ledBoth.green)
            self.ledBoth.currentBlue = self.colorScale(self.ledBoth.blue)
            self.ledBoth.currentIntensity = self.ledBoth.intensity
        self.lock1.release()

    def reportRed(self):
        self.lock1.acquire()
        return_value = self.ledBoth.red
        self.lock1.release()
        return return_value

    def reportGreen(self):
        self.lock1.acquire()
        return_value = self.ledBoth.green
        self.lock1.release()
        return return_value

    def reportBlue(self):
        self.lock1.acquire()
        return_value = self.ledBoth.blue
        self.lock1.release()
        return return_value

    def reportBrightness(self):
        self.lock1.acquire()
        return_value = self.ledBoth.intensity
        self.lock1.release()
        return return_value

    def reportTime(self):
        self.lock1.acquire()
        return_value = self.ledBoth.time
        self.lock1.release()
        return return_value
