import camera_control
import led_control
import matrix_control
import pumpkin_audio
import temperature_reader

class Peripherals:

    def __init__(self, sendQueue):
        print("Peripherals initialization")
        matrix_control.MatrixControl(sendQueue)
        led_control.LedControl(sendQueue)
        pumpkin_audio.PumpkinAudio(sendQueue)
        temperature_reader.TemperatureSensor(sendQueue)

    def set_value_mouth__text(self, value):
        matrix_control.setText(value)

    def set_value_eyes__red(self, value):
        led_control.setLedRed(value)

    def set_value_eyes__green(self, value):
        led_control.setLedGreen(value)

    def set_value_eyes__blue(self, value):
        led_control.setLedBlue(value)

    def set_value_eyes__brightness(self, value):
        led_control.setLedBrightness(value)

    def set_value_eyes__pulse(self, value):
        led_control.setLedTime(value)

    def set_value_nose__x(self, value):
        camera_control.setX(value)

    def set_value_nose__y(self, value):
        camera_control.setY(value)

    def get_value_mouth__text(self):
        matrix_control.getText()

    def get_value_eyes__red(self):
        return led_control.reportRed()

    def get_value_eyes__green(self):
        return led_control.reportGreen()

    def get_value_eyes__blue(self):
        return led_control.reportBlue()

    def get_value_eyes__brightness(self):
        return led_control.reportBrightness()

    def get_value_eyes__pulse(self):
        return reportTime

    def get_value_nose__image(self):
        return camera_control.takePicture()

    def get_value_nose__x(self):
        return camera_control.reportX()

    def get_value_nose__y(self):
        return camera_control.reportY()

    def get_value_tongue__temperature(self):
        return temperature_reader.getTemperature()

