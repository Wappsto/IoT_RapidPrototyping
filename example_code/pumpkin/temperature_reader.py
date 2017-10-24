#!/usr/bin/python3

import time
import threading
import queue
import generic.send_data as send_data
import uuid_defines as my_ids

path = "/sys/bus/w1/devices/28-0416XXXXXXX/w1_slave" TODO

class TemperatureSensor():

    def __init__(self, queue):
        self.tempThread = threading.Thread(target=self.readThread)
        self.tempThread.setDaemon(True)
        self.tempThread.start()
        self.sendToQueue = queue
        self.celcius = 0
        self.lastSentValue = 0
        self.update = True
        self.lock = threading.Lock()
        self.differenceToTriggerReport = 1

    def readThread(self):
        while True:
            sensorFile = open(path, "r")
            data = sensorFile.readlines()
            sensorFile.close()
            if data[0].strip()[-3:] == "YES":
                #can I find a temperature (t=)
                equals_pos = data[1].find("t=")
                if equals_pos != -1:
                    tempData = data[1][equals_pos+2:]
                    self.lock.acquire()
                    self.celcius = float(tempData) / 1000
                    if self.update and (abs(self.celcius - self.lastSentValue) > self.differenceToTriggerReport):
                        print("Sending temperature: %f" % self.celcius)
                        self.lastSentValue = self.celcius
                        report = send_data.SendData(send_data.SEND_REPORT, data=str(self.celcius), network_id=my_ids.NETWORK_ID, device_id=my_ids.TODO, value_id=my_ids.TODO, state_id=my_ids.TODO)
                        self.sendToQueue.put(report)
                    #print(self.celcius)
                    self.lock.release()
                else:
                    print('Did not find t=: %s' % str(data))
            else:
                print('Did not find yes: %s' % str(data))
            time.sleep(1)

    def getTemperature(self):
        self.lock.acquire()
        print("Replying with temperature: %f" % self.celcius)
        returnValue = self.celcius
        self.lock.release()
        return returnValue

