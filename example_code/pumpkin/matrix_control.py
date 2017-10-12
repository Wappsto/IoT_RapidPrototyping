#!/usr/bin/env python

import max7219.led as led
from max7219.font import CP437_FONT, proportional
import time
#, SINCLAIR_FONT, TINY_FONT,
#from random import randrange
import queue
import threading
import generic.send_data as send_data
import uuid_defines as my_ids

device = led.matrix(cascaded=4)


class DataInputText():

    def __init__(self, text, intensity):
        self.text = text
        self.intensity = intensity


class MatrixControl():

    def __init__(self, sendingQueue):
        self.textQueue = queue.Queue(maxsize=0)
        #self.queueThread = threading.Thread(target=self.writeThread)
        self.lock = threading.Lock()
        self.intensity = 100
        self.text = ""

        self.queueThread = threading.Thread(target=self.continuousThreadQueue)
        self.queueThread.setDaemon(True)
        self.queueThread.start()

        self.writeThread = threading.Thread(target=self.continousWriteThread)
        self.writeThread.setDaemon(True)
        self.writeThread.start()

        self.sendToQueue = sendingQueue

    def continousWriteThread(self):
        while True:
            self.lock.acquire()
            using = self.intensity / 6.666
            #print(using)
            #print(int(using))
            device.brightness(int(using))
            device.scroll_down()
            device.orientation(90)
            device.show_message(self.text, font=proportional(CP437_FONT))
            self.lock.release()
            time.sleep(1)

    def continuousThreadQueue(self):
        while True:
            values = self.textQueue.get()
            self.lock.acquire()
            self.text = values.text
            self.lock.release()
            self.textQueue.task_done()

    def setText(self, text, intensity=100):
        newText = DataInputText(text, intensity)
        self.textQueue.put(newText, block=False)

    def getText(self):
        self.lock.acquire()
        returnValue = self.text
        self.lock.release()
        return returnValue
