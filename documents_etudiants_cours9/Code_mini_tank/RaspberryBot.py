import socket
import time
import sys
import Led
import RobotMovement 
import CameraMovement
import Honk
import Dispatcher
import Ultrasonic
import Tracking
import Autopilot
import RPi.GPIO as GPIO
import select

HOST_IP = "192.168.4.1"
HOST_PORT = 7654
SOCKET_ALIVE = False
SOCKET_TCP = None
SOCKET_CON = None
INITIALIZED_GPIO = False
ALREADY_CONNECTED = False

def initializeRobot():
    
    global HOST_IP
    global HOST_PORT
    
    initServer(HOST_IP, HOST_PORT)

def initServer(HOST_IP, HOST_PORT):
    global SOCKET_CON
    global SOCKET_TCP
    global SOCKET_ALIVE
    global INITIALIZED_GPIO
    if SOCKET_ALIVE == False : 
        try:
            while True:
                initSocket()
                try:
                    attemptConnection()
                except socket.timeout:
                    print("Connection timeout, restarting procedure...")
                while SOCKET_ALIVE:
                    try:
                        data = SOCKET_CON.recv(1024)
                        SOCKET_ALIVE = Dispatcher.dispatch(data, SOCKET_CON)
                    except socket.timeout as e:
                        print(e)
                        data = '{"cmd" : "disconnect"}'
                        SOCKET_ALIVE = Dispatcher.dispatch(data.encode(), SOCKET_CON)
                    except ConnectionResetError:
                        print("CONNECTION ERROR WHEN CLOSE APP WITHOUT DISCONNECTION")
                        SOCKET_ALIVE = False
                if INITIALIZED_GPIO:        
                    shutdownProcess()
        except KeyboardInterrupt:
            if INITIALIZED_GPIO:        
                shutdownProcess()
            
def initSocket():
    
    global HOST_IP
    global HOST_PORT
    global SOCKET_ALIVE
    global SOCKET_TCP
    
    SOCKET_TCP = None
    SOCKET_CON = None
    SOCKET_TIME_OUT = 2
    SOCKET_ALIVE = False
    print("Starting sockets: TCP...")
    socket.setdefaulttimeout(SOCKET_TIME_OUT)
    SOCKET_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_addr = (HOST_IP, HOST_PORT)
    socketInitBool = False
    while socketInitBool == False:
        try:
            SOCKET_TCP.bind(host_addr) 
            SOCKET_TCP.listen(1)
            print("Server is listening on %s:%d!" %(HOST_IP, HOST_PORT) )
            socketInitBool = True
        except socket.error as e:
            socketInitBool = False

    
def attemptConnection():
    
    global SOCKET_CON
    global SOCKET_TCP
    global SOCKET_ALIVE
    
    print ('Waiting for connection...')
    SOCKET_CON, (client_ip, client_port) = SOCKET_TCP.accept()
    print("Client: %s  is connecting to RaspberryBot" %client_ip)
    send_connect_ping()
    SOCKET_ALIVE = True
    initGPIO()

def initGPIO():   
    
    global INITIALIZED_GPIO
    
    INITIALIZED_GPIO = True
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    Led.initLed()
    RobotMovement.initRobotMovement()
    CameraMovement.initCameraMovement()
    Ultrasonic.initUltraSonic()
    Tracking.initFollowLine()
    
def shutdownGPIO():
    Led.shutdownLedGPIO()
    RobotMovement.shutdownRobotMovementGPIO()
    CameraMovement.shutdownCameraMovementGPIO()
    Ultrasonic.shutdownUltraSonicGPIO()
    GPIO.cleanup()
    
def shutdownThread():
    Led.shutdownThreadLed()
    CameraMovement.shutdownThreadCameraMovement()
    Honk.shutdownThreadHonk()
    Ultrasonic.shutdownThreadUltraSonic()
    Tracking.shutdownThreadFollowLine()
    Autopilot.shutdownThreadAutoPilot()
    RobotMovement.shutdownThreadRobotMovement()

def shutdownProcess():
    global INITIALIZED_GPIO
    global SOCKET_CON
    
    INITIALIZED_GPIO = False
    SOCKET_CON.close()
    shutdownThread()
    time.sleep(0.2)
    shutdownGPIO()
    
def send_connect_ping():
    global SOCKET_CON
    
    dataToSend = '{"cmd" : "connection"}'
    SOCKET_CON.send(dataToSend.encode())

initializeRobot()