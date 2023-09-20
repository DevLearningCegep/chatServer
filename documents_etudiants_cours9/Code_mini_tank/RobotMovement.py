import RPi.GPIO as GPIO
import threading
import time

PIN_FL = 20
PIN_RL = 21
PIN_FR = 19
PIN_RR = 26

PIN_L_SPEED = 16
PIN_R_SPEED = 13

PWM_L_SPEED = None
PWM_R_SPEED = None

movementThread = None

class RobotMovementThread (threading.Thread):
    def __init__(self, LEFT_STATE, RIGHT_STATE, L_SPEED_VALUE, R_SPEED_VALUE):
        threading.Thread.__init__(self)
        self.LEFT_STATE = LEFT_STATE
        self.RIGHT_STATE = RIGHT_STATE
        self.L_SPEED_VALUE = L_SPEED_VALUE
        self.R_SPEED_VALUE = R_SPEED_VALUE
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet() 
    
    def run(self):
        
        global PWM_L_SPEED
        global PWM_R_SPEED

        while True:
            if self.stopped():
                return
            GPIO.output(PIN_FL, self.LEFT_STATE)
            GPIO.output(PIN_RL, not self.LEFT_STATE)
            GPIO.output(PIN_FR, self.RIGHT_STATE)
            GPIO.output(PIN_RR, not self.RIGHT_STATE)

            PWM_L_SPEED.ChangeDutyCycle(abs(float(self.L_SPEED_VALUE)))
            PWM_R_SPEED.ChangeDutyCycle(abs(float(self.R_SPEED_VALUE)))
            
            time.sleep(0.05)
            
    def changeValue(self, LEFT_STATE, RIGHT_STATE, L_SPEED_VALUE, R_SPEED_VALUE):

        self.LEFT_STATE = LEFT_STATE
        self.RIGHT_STATE = RIGHT_STATE
        self.L_SPEED_VALUE = L_SPEED_VALUE
        self.R_SPEED_VALUE = R_SPEED_VALUE


def getMotorSpeed(angle, strength):
    invert = False
    if angle > 100 and angle < 260:
        invert = True
    angle = ((-angle + 180) % 360) - 180
    strength = min(max(0, strength), 100)
    v_a = strength * (45 - angle % 90) / 45          
    v_b = min(100, 2 * strength + v_a, 2 * strength - v_a) 
    if angle < -90: 
        if not invert:
            return -v_b, -v_a
        else: 
            return -v_a, -v_b
    if angle < 0:   return -v_a, v_b
    if angle < 90:  return v_b, v_a
    if not invert:
        return v_a, -v_b              
    else:
        return -v_b, v_a

def changeSpeed(angle, strength):
    global movementThread
    
    speedTable = getMotorSpeed(angle, strength)
    leftMotorState = getMotorState(speedTable[0])
    rightMotorState = getMotorState(speedTable[1])
    if movementThread != None:
        movementThread.changeValue(leftMotorState, rightMotorState, speedTable[0], speedTable[1])
    else:
        movementThread = RobotMovementThread(leftMotorState, rightMotorState, speedTable[0], speedTable[1])
        movementThread.start()
        
def getMotorState(speed):
    state = None
    if speed < 0:
        state = False
    else:
        state = True
    return state

def initRobotMovement():
    
    global PIN_FL
    global PIN_RL
    global PIN_FR
    global PIN_RR

    global PIN_L_SPEED
    global PIN_R_SPEED

    global PWM_L_SPEED
    global PWM_R_SPEED
    
    GPIO.setup(PIN_FL, GPIO.OUT)
    GPIO.setup(PIN_RL, GPIO.OUT)
    GPIO.setup(PIN_FR, GPIO.OUT)
    GPIO.setup(PIN_RR, GPIO.OUT)
    
    GPIO.setup(PIN_L_SPEED, GPIO.OUT)
    GPIO.setup(PIN_R_SPEED, GPIO.OUT)
    
    PWM_L_SPEED = GPIO.PWM(PIN_L_SPEED, 2000)
    PWM_R_SPEED = GPIO.PWM(PIN_R_SPEED, 2000)
    
    PWM_L_SPEED.start(0)
    PWM_R_SPEED.start(0)


def shutdownRobotMovementGPIO():
    
    global PWM_L_SPEED
    global PWM_R_SPEED
    
    PWM_L_SPEED.stop()
    PWM_R_SPEED.stop()
    PWM_L_SPEED = None
    PWM_R_SPEED = None
    
def shutdownThreadRobotMovement():
    global movementThread
    if movementThread != None:
        movementThread.stop()
        movementThread = None  
