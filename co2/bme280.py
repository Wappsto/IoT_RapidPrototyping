import time
import smbus2
from collections import namedtuple

def setup_settings():
    osrs_t = 1  # Temperature oversampling x 1
    osrs_p = 1  # Pressure oversampling x 1
    osrs_h = 1  # Humidity oversampling x 1
    mode = 3  # Normal mode
    t_sb = 5  # Tstandby 1000ms
    bme280filter = 0  # Filter off
    spi3w_en = 0  # 3-wire SPI Disable
    ctrl_meas_reg = (osrs_t << 5) | (osrs_p << 2) | mode
    config_reg = (t_sb << 5) | (bme280filter << 2) | spi3w_en
    ctrl_hum_reg = osrs_h
    return config_reg, ctrl_hum_reg, ctrl_meas_reg


class BME280():
    def __init__(self, setup_run=False):
        super(BME280, self).__init__()

        self.i2c_address = 0x77
        self.bus_number = smbus2.SMBus(1)
        self.setup_run = setup_run
        self.calibration_h = []
        self.calibration_p = []
        self.calibration_t = []
        self.t_fine = 0.0
        self.Data = namedtuple('Data', ['humidity', 'pressure', 'temperature'])

        if not self.setup_run:
            config_reg, ctrl_hum_reg, ctrl_meas_reg = setup_settings()
            self.write_byte(0xF2, ctrl_hum_reg)
            self.write_byte(0xF4, ctrl_meas_reg)
            self.write_byte(0xF5, config_reg)
            self.populate_calibration_data()
            self.setup_run = True

    def read_byte(self, cmd):
        return self.bus_number.read_byte_data(self.i2c_address, cmd)

    def write_byte(self, cmd, value):
        return self.bus_number.write_byte_data(self.i2c_address, cmd, value)

    def reset_calibration(self):
        self.calibration_h = []
        self.calibration_p = []
        self.calibration_t = []
        self.t_fine = 0.0

    def populate_calibration_data(self):
        raw_data = []
        for i in range(0x88, 0x88 + 24):
            raw_data.append(self.read_byte(i))

        raw_data.append(self.read_byte(0xA1))

        for i in range(0xE1, 0xE1 + 7):
            raw_data.append(self.read_byte(i))

        for i in range(0, 6, 2):
            self.calibration_t.append((raw_data[i + 1] << 8) | raw_data[i])

        for i in range(6, 24, 2):
            self.calibration_p.append((raw_data[i + 1] << 8) | raw_data[i])

            self.calibration_h.append(raw_data[24])
            self.calibration_h.append((raw_data[26] << 8) | raw_data[25])
            self.calibration_h.append(raw_data[27])
            self.calibration_h.append((raw_data[28] << 4) | (0x0F & raw_data[29]))
            self.calibration_h.append((raw_data[30] << 4) | ((raw_data[29] >> 4) & 0x0F))
            self.calibration_h.append(raw_data[31])
        for i in range(1, 2):
            if self.calibration_t[i] & 0x8000:
                self.calibration_t[i] = (-self.calibration_t[i] ^ 0xFFFF) + 1
        for i in range(1, 8):
            if self.calibration_p[i] & 0x8000:
                self.calibration_p[i] = (-self.calibration_p[i] ^ 0xFFFF) + 1
        for i in range(0, 6):
            if self.calibration_h[i] & 0x8000:
                self.calibration_h[i] = (-self.calibration_h[i] ^ 0xFFFF) + 1

    def read_adc(self):
        data = []
        for i in range(0xF7, 0xF7 + 8):
            data.append(self.read_byte(i))

        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw = (data[6] << 8) | data[7]
        return self.Data(hum_raw, pres_raw, temp_raw)

    def read_all(self, ):
        data = self.read_adc()
        return self.Data(self.read_humidity(data), self.read_pressure(data), self.read_temperature(data))

    def read_humidity(self, data=None):
        if data is None:
            data = self.read_adc()
            # We need a temperature reading to calculate humidity
            self.read_temperature(data)
        return self.compensate_humidity(data.humidity)

    def read_pressure(self, data=None):
        if data is None:
            data = self.read_adc()
            # We need a temperature reading to calculate pressure
            self.read_temperature(data)
        return self.compensate_pressure(data.pressure)

    def read_temperature(self, data=None):
        if data is None:
            data = self.read_adc()
        return self.compensate_temperature(data.temperature)

    def compensate_pressure(self, adc_p):
        v1 = (self.t_fine / 2.0) - 64000.0
        v2 = (((v1 / 4.0) * (v1 / 4.0)) / 2048) * self.calibration_p[5]
        v2 += ((v1 * self.calibration_p[4]) * 2.0)
        v2 = (v2 / 4.0) + (self.calibration_p[3] * 65536.0)
        v1 = (((self.calibration_p[2] * (((v1 / 4.0) * (v1 / 4.0)) / 8192)) / 8) + (
                (self.calibration_p[1] * v1) / 2.0)) / 262144
        v1 = ((32768 + v1) * self.calibration_p[0]) / 32768
        if v1 == 0:
            return 0
        pressure = ((1048576 - adc_p) - (v2 / 4096)) * 3125
        if pressure < 0x80000000:
            pressure = (pressure * 2.0) / v1
        else:
            pressure = (pressure / v1) * 2
        v1 = (self.calibration_p[8] * (((pressure / 8.0) * (pressure / 8.0)) / 8192.0)) / 4096
        v2 = ((pressure / 4.0) * self.calibration_p[7]) / 8192.0
        pressure += ((v1 + v2 + self.calibration_p[6]) / 16.0)
        return pressure / 100

    def compensate_temperature(self, adc_t):
        v1 = (adc_t / 16384.0 - self.calibration_t[0] / 1024.0) * self.calibration_t[1]
        v2 = (adc_t / 131072.0 - self.calibration_t[0] / 8192.0) * (adc_t / 131072.0 - self.calibration_t[0] / 8192.0) * \
             self.calibration_t[2]
        t_fine = v1 + v2
        temperature = t_fine / 5120.0
        return temperature

    def compensate_humidity(self, adc_h):
        var_h = self.t_fine - 76800.0
        if var_h == 0:
            return 0
        var_h = (adc_h - (self.calibration_h[3] * 64.0 + self.calibration_h[4] / 16384.0 * var_h)) * (
                self.calibration_h[1] / 65536.0 * (1.0 + self.calibration_h[5] / 67108864.0 * var_h * (
                1.0 + self.calibration_h[2] / 67108864.0 * var_h)))
        var_h *= (1.0 - self.calibration_h[0] * var_h / 524288.0)
        if var_h > 100.0:
            var_h = 100.0
        elif var_h < 0.0:
            var_h = 0.0
        return var_h


if __name__ == "__main__":

    try:
        bme280 = BME280()

        while(1):
            print(bme280.read_all())
            print(bme280.read_pressure())
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Stopped")
