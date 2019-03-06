from handlers import send__Report
import uuid_defines as my_ids
import RPi.GPIO as GPIO

ledPin = 17

class ThreadExample:

    def __init__(self, send_queue):
        self.uuid = my_ids.UUID()
        self.sendToQueue = send_queue
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ledPin, GPIO.OUT)
        GPIO.output(ledPin, GPIO.LOW)

    def get_value(self):
        return_value = GPIO.input(ledPin)
        return return_value

    def set_value(self, value):
        if value=="0":
            GPIO.output(ledPin, GPIO.LOW)
            print("off")

        else:
            GPIO.output(ledPin, GPIO.HIGH)
            print("on")

        send__Report(value, self.sendToQueue, self.uuid.NETWORK_ID, self.uuid.getbulb_led())


