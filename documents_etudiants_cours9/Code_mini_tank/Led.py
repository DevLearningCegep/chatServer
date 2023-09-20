import RPi.GPIO as GPIO
import threading
import time

PIN_LED_R = 22
PIN_LED_G = 27
PIN_LED_B = 24

PWM_LED_R = None
PWM_LED_G = None
PWM_LED_B = None

colorThread = None

class LedThread (threading.Thread):
    def __init__(self, LED_R_VALUE, LED_G_VALUE, LED_B_VALUE):
        threading.Thread.__init__(self)
        self.LED_R_VALUE = LED_R_VALUE
        self.LED_G_VALUE = LED_G_VALUE
        self.LED_B_VALUE = LED_B_VALUE
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet() 
    
    def run(self):
        global PWM_LED_R
        global PWM_LED_G
        global PWM_LED_B

        while True:
            if self.stopped():
                return
            PWM_LED_R.ChangeDutyCycle(float(self.LED_R_VALUE) * 100)
            PWM_LED_G.ChangeDutyCycle(float(self.LED_G_VALUE) * 100)
            PWM_LED_B.ChangeDutyCycle(float(self.LED_B_VALUE) * 100)
            time.sleep(0.5)
    
    def changeValue(self, LED_R_VALUE, LED_G_VALUE, LED_B_VALUE):
        print(self.LED_R_VALUE, self.LED_G_VALUE, self.LED_B_VALUE)
        self.LED_R_VALUE = LED_R_VALUE
        self.LED_G_VALUE = LED_G_VALUE
        self.LED_B_VALUE = LED_B_VALUE
            
def changeColor(LED_STATE, LED_R_VALUE, LED_G_VALUE, LED_B_VALUE):
    global colorThread
    if LED_STATE:
        if colorThread != None:
            colorThread.changeValue(LED_R_VALUE, LED_G_VALUE, LED_B_VALUE)
        else:
            colorThread = LedThread(LED_R_VALUE, LED_G_VALUE, LED_B_VALUE)
            colorThread.start()
    else:
        if  colorThread != None:
            colorThread.changeValue(0, 0, 0)
            
def initLed():
    
    global PWM_LED_R
    global PWM_LED_G
    global PWM_LED_B

    global PIN_LED_R
    global PIN_LED_G
    global PIN_LED_B
    
    GPIO.setup(PIN_LED_R, GPIO.OUT)
    GPIO.setup(PIN_LED_G, GPIO.OUT)
    GPIO.setup(PIN_LED_B, GPIO.OUT)

    PWM_LED_R = GPIO.PWM(PIN_LED_R, 1000)
    PWM_LED_G = GPIO.PWM(PIN_LED_G, 1000)
    PWM_LED_B = GPIO.PWM(PIN_LED_B, 1000)
    
    PWM_LED_R.start(0)
    PWM_LED_G.start(0)
    PWM_LED_B.start(0)

def shutdownLedGPIO():
    global PWM_LED_R
    global PWM_LED_G
    global PWM_LED_B
    
    PWM_LED_R.stop()
    PWM_LED_G.stop()
    PWM_LED_B.stop()
    
    PWM_LED_R = None
    PWM_LED_G = None
    PWM_LED_B = None
    
    
def shutdownThreadLed():
    global colorThread
    if colorThread != None:
        colorThread.stop()
        colorThread = None
    