import camera_control
import led_control
import matrix_control
import pumpkin_audio
import temperature_reader

class Peripherals:

    def __init__(self, sendQueue):
        print("Peripherals initialization")
        self.matrix = matrix_control.MatrixControl(sendQueue)
        self.led = led_control.LedControl(sendQueue)
        self.audio = pumpkin_audio.PumpkinAudio(sendQueue)
        self.temperature = temperature_reader.TemperatureSensor(sendQueue)
        self.camera = camera_control.CameraControl(sendQueue)

    def set_value_mouth__text(self, value):
        self.matrix.setText(value)

    def set_value_eyes__red(self, value):
        self.led.setLedRed(value)

    def set_value_eyes__green(self, value):
        self.led.setLedGreen(value)

    def set_value_eyes__blue(self, value):
        self.led.setLedBlue(value)

    def set_value_eyes__brightness(self, value):
        self.led.setLedBrightness(value)

    def set_value_eyes__pulse(self, value):
        self.led.setLedTime(value)

    def set_value_nose__x(self, value):
        self.camera.setX(value)

    def set_value_nose__y(self, value):
        self.camera.setY(value)

    def get_value_mouth__text(self):
        return self.matrix.getText()

    def get_value_eyes__red(self):
        return self.led.reportRed()

    def get_value_eyes__green(self):
        return self.led.reportGreen()

    def get_value_eyes__blue(self):
        return self.led.reportBlue()

    def get_value_eyes__brightness(self):
        return self.led.reportBrightness()

    def get_value_eyes__pulse(self):
        return self.led.getLedTime()

    def get_value_nose__image(self):
        self.camera.takePicture()
        return 0

    def get_value_nose__x(self):
        return self.camera.reportX()

    def get_value_nose__y(self):
        return self.camera.reportY()

    def get_value_tongue__temperature(self):
        return self.temperature.getTemperature()

