import pygame
import time
import threading
import queue
import os

import uuid_defines as my_ids
import generic.send_data as send_data

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
laughter = ROOT_PATH + "/Evil_Laugh_1-Timothy-64737261.mp3"
scream = ROOT_PATH + "/scream_error.wav"

audio_list = {
    0: 'no audio/stop',
    1: laughter,
    2: scream
}

class PumpkinAudio:

    def __init__(self, sendQueue):
        pygame.mixer.init()

        self.volume = 100
        self.playingId = 0

        self.threadEvent = threading.Thread(target=self.eventThread)
        self.threadEvent.setDaemon(True)
        self.threadEvent.start()
        self.sendToQueue = sendQueue
        self.audioLock = threading.Lock()

        pygame.mixer.music.set_volume(self.volume/100.0)

    def eventThread(self):
        send_event_when_stop = False
        while True:
            if pygame.mixer.music.get_busy():
                send_event_when_stop = True
            else:
                if send_event_when_stop:
                    self.audioLock.acquire()
                    self.sendReportPlayingStopped()
                    send_event_when_stop = False
                    self.playingId = 0
                    self.audioLock.release()
            time.sleep(0.1)

    def setAudio(self, id):
        if id in audio_list:
            self.audioLock.acquire()
            self.playingId = id
            self.audioLock.release()
            pygame.mixer.music.stop()

            if id > 0:
                pygame.mixer.music.load(audio_list.get(id))
                print("Loading %s" % audio_list.get(id))
                pygame.mixer.music.play()
                #time.sleep(2)
        else:
            print("Error: id %d not in audio list" % id)

    def getAudio(self):
        self.audioLock.acquire()
        return_value = self.playingId
        self.audioLock.release()
        return return_value


    def sendReportPlayingStopped(self):
        print("Playing has stopped")
        report = send_data.SendData(send_data.SEND_REPORT, data="0", network_id=my_ids.NETWORK_ID, device_id=my_ids.AUDIO__DEVICE_ID, value_id=my_ids.AUDIO__PLAY__VALUE_ID, state_id=my_ids.AUDIO__PLAY__STATE_REPORT_ID)
        self.sendToQueue.put(report)

    def setVolume(self, volume):
        # pygame vol 0.0-1.0 ours 0-100
        self.audioLock.acquire()
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume/100.0)
        self.audioLock.release()

    def getVolume(self):
        self.audioLock.acquire()
        return_value = self.volume
        self.audioLock.release()
        return return_value


# For testing
if __name__ == "__main__":
    temp_queue = queue.Queue(maxsize=0)
    test = PumpkinAudio(temp_queue)

    while True:
        try:

            test.setAudio(1)
            time.sleep(3)

            test.setAudio(2)

            time.sleep(2)
            test.setAudio(0)

            time.sleep(2)

        except KeyboardInterrupt:
            test.setAudio(0)
            break

    time.sleep(1)