enableCamera = True
if enableCamera:
    from picamera import PiCamera
import os
import threading
import queue
import uuid_defines as my_ids
import base64
import generic.send_data as send_data
#from time import sleep
import pumpkin_audio

baseDir, baseFile = os.path.split(os.path.abspath(__file__))
FILENAME = baseDir + "/pumpkin.jpg"

class CameraControl():

    def __init__(self, socketQueue):
        if enableCamera:
            self.camera = PiCamera()
            self.camera.led = False
        else:
            self.camera = None
        self.triggerQueue = queue.Queue(maxsize=0)
        self.respondQueue = socketQueue
        self.camThread = threading.Thread(target=self.cameraThread)
        self.camThread.setDaemon(True)
        self.camThread.start()
        self.resolution_x = 160
        self.resolution_y = 120
        self.lock = threading.Lock()
        self.audio = pumpkin_audio.PumpkinAudio(None)

    def cameraThread(self):
        while True:
            #self.camera.start_preview()
            #sleep(1)
            self.triggerQueue.get()
            print("trigger")
            self.lock.acquire()
            if enableCamera:
                self.camera.led = False
                self.camera.capture(FILENAME, resize=(self.resolution_x, self.resolution_y))
            self.lock.release()
            #camera.stop_preview()
            sendData = send_data.SendData(send_data.SEND_REPORT)
            imageBytes = open(FILENAME, "rb").read()
            imageBase64 = base64.b64encode(imageBytes)
            sendData.data = "data:image/jpg;base64,"+imageBase64.decode('utf-8')
            sendData.network_id = my_ids.NETWORK_ID
            sendData.device_id = my_ids.NOSE__DEVICE_ID
            sendData.value_id = my_ids.camera_value_id TODO
            sendData.state_id = my_ids.camera_report_id TODO
            #sendData.hexSize = os.stat(FILENAME).st_size
            self.respondQueue.put(sendData)
            self.triggerQueue.task_done()
            self.audio.setAudio(1)


            #print(open('foo.jpg', "rb").read())

    def takePicture(self):
        self.triggerQueue.put(None)

    def setX(self, x_value):
        self.lock.acquire()
        self.resolution_x = x_value
        self.lock.release()

    def setY(self, y_value):
        self.lock.acquire()
        self.resolution_y = y_value
        self.lock.release()

    def reportX(self):
        self.lock.acquire()
        return_value = self.resolution_x
        self.lock.release()
        return return_value

    def reportY(self):
        self.lock.acquire()
        return_value = self.resolution_y
        self.lock.release()
        return return_value
