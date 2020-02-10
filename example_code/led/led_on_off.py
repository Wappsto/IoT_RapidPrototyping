
# Initialize
# requires: sudo apt-get install rpi.gpio
import RPi.GPIO as GPIO
led_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)




# replace "def value_callback(the_value, action_type):" with this
def led_value_callback(value, action_type):
    if action_type == 'refresh':
        msg = "Refreshing led value: {}".format(value.name)
        wapp_log.info(msg)
        value.update(GPIO.input(led_pin))
    elif action_type == 'set':
        msg = "Set value: {} to {}.".format(value.name, value.last_controlled)
        wapp_log.info(msg)
        if value.last_controlled == "0":
            GPIO.output(led_pin, GPIO.LOW)
        else:
            GPIO.output(led_pin, GPIO.HIGH)
        value.update(GPIO.input(led_pin))




# replace "for device in service.instance.device_list:"-loop with this:
led_device = service.get_device("Bulb")
led_value = led_device.get_value("LED")
led_value.set_callback(led_value_callback)
