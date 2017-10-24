import camera_control
import led_control
import matrix_control
import pumpkin_audio
import temperature_reader

class Peripherals:

    def __init__(self, sendQueue):
        print("Peripherals initialization")
        self.matrix_control.MatrixControl(sendQueue)
        self.led_control.LedControl(sendQueue)
        self.pumpkin_audio.PumpkinAudio(sendQueue)
        self.temperature_reader.TemperatureSensor(sendQueue)

    def set_value_mouth__text(self, value):
        matrix_control.setText(value)

    def set_value_eyes__red(self, value):
        self.led_control.setLedRed(value)

    def set_value_eyes__green(self, value):
        self.led_control.setLedGreen(value)

    def set_value_eyes__blue(self, value):
        self.led_control.setLedBlue(value)

    def set_value_eyes__brightness(self, value):
        self.led_control.setLedBrightness(value)

    def set_value_eyes__pulse(self, value):
        self.led_control.setLedTime(value)

    def set_value_nose__x(self, value):
        self.camera_control.setX(value)

    def set_value_nose__y(self, value):
        self.camera_control.setY(value)

    def get_value_mouth__text(self):
        return self.matrix_control.getText()

    def get_value_eyes__red(self):
        return self.led_control.reportRed()

    def get_value_eyes__green(self):
        return self.led_control.reportGreen()

    def get_value_eyes__blue(self):
        return self.led_control.reportBlue()

    def get_value_eyes__brightness(self):
        return self.led_control.reportBrightness()

    def get_value_eyes__pulse(self):
        return self.led_control.getLedTime()

    def get_value_nose__image(self):
        self.camera_control.takePicture()
        return 0

    def get_value_nose__x(self):
        return self.camera_control.reportX()

    def get_value_nose__y(self):
        return self.camera_control.reportY()

    def get_value_tongue__temperature(self):
        return self.temperature_reader.getTemperature()

