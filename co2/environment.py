import time
import threading

if __name__ == "__main__":
    from bme280 import BME280
    from scd30 import SCD30
    import queue
else:
    from values.bme280 import BME280
    from values.scd30 import SCD30
    import uuid_defines as my_ids
    from handlers import send__Report


class Environment:

    def __init__(self, send_queue):
        self.sendToQueue = send_queue
        self.uuid = my_ids.UUID()

        self.bme280 = BME280()
        self.measurement_interval = 60
        auto_calibration = 1
        self.scd30 = SCD30(self.measurement_interval, auto_calibration, int(self.bme280.read_pressure()))

        self.lock = threading.Lock()
        self.current_pressure = None
        self.current_scd30_data = None

        self.readThread = threading.Thread(target=self.read_thread)
        self.readThread.setDaemon(True)
        self.readThread.start()

    def read_thread(self):
        time.sleep(2)
        while True:
            if self.scd30.data_ready():
                updated_data = False
                self.lock.acquire()
                self.current_pressure = self.bme280.read_pressure()
                test = self.scd30.get_scd30_measurements()
                if test:
                    self.current_scd30_data = test
                    update_data = True
                else:
                    print("Not valid SCD30 data")

                if update_data:
                    self.send_report()
                self.lock.release()
            else:
                print("SCD30 data not ready")

            time.sleep(self.measurement_interval)

    def send_report(self):
        send__Report(self.current_scd30_data.CO2, self.sendToQueue, self.uuid.NETWORK_ID, self.uuid.getsensors_co2())
        send__Report(self.current_scd30_data.temperature, self.sendToQueue, self.uuid.NETWORK_ID, self.uuid.getsensors_temperature())
        send__Report(self.current_pressure, self.sendToQueue, self.uuid.NETWORK_ID, self.uuid.getsensors_pressure())
        send__Report(self.current_scd30_data.humidity, self.sendToQueue, self.uuid.NETWORK_ID, self.uuid.getsensors_humidity())

    def get_pressure(self):
        self.lock.acquire()
        return_value = self.current_pressure
        self.lock.release()
        return return_value

    def get_temperature(self):
        self.lock.acquire()
        return_value = self.current_scd30_data.temperature
        self.lock.release()
        return return_value

    def get_humidity(self):
        self.lock.acquire()
        return_value = self.current_scd30_data.humidity
        self.lock.release()
        return return_value

    def get_co2(self):
        self.lock.acquire()
        return_value = self.current_scd30_data.CO2
        self.lock.release()
        return return_value


if __name__ == "__main__":

    try:
        sendingQueue = queue.Queue(maxsize=0)
        env = Environment(sendingQueue)

        while(1):
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("Stopped")
