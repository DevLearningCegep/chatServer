import RPi.GPIO as GPIO
import threading
import time

PIN_HONK = 8

HONK = None

buzzerThread = None

class HonkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet() 
    
    def run(self):
        global buzzerThread
        
        GPIO.setup(PIN_HONK,GPIO.OUT)
        time.sleep(3)
        GPIO.setup(PIN_HONK,GPIO.IN)
        buzzerThread = None

def buzz():
    global buzzerThread
    
    buzzerThread = HonkThread()
    buzzerThread.start()
    
def shutdownThreadHonk():
    global buzzerThread
    if buzzerThread != None:
        GPIO.setup(PIN_HONK,GPIO.IN)
        buzzerThread.stop()
        buzzerThread = None