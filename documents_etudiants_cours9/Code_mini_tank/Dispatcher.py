import Led 
import json
import RobotMovement
import Honk
import CameraMovement
import Ultrasonic
import Tracking
import Autopilot

def dispatch(data, socket_con):
    command = None
    SOCKET_STATE = True
    if (data.decode() and not data.decode().isspace()):
        try:
            commandJSONArray = separateMultipleJSON(data.decode())
            for i in commandJSONArray:
                dataJson = json.loads(i)
                SOCKET_STATE = attemptCommand(socket_con,dataJson)
        except ValueError as e:
            print(e)
            dataToSend = '{"cmd" : "disconnect"}'
            sendData(socket_con, dataToSend)
            SOCKET_STATE = False
    return SOCKET_STATE


def separateMultipleJSON(data):
    jsonArray = []
    index = 0
    while index != -1:
        index = data.find('}')
        if index != -1:
            newJSON = data[:index + 1]
            if newJSON.find('{') != -1 :
                jsonArray.append(newJSON)
            data = data[index + 1:]
    return jsonArray
    
def attemptCommand(socket_con, dataJson):
    SOCKET_STATE = True
    command = dataJson["cmd"]
    if command != None:
        if command == "color":
            changeLedColor(dataJson)
        elif command == "disconnect":
            dataToSend = '{"cmd" : "disconnect"}'
            sendData(socket_con, dataToSend)
            SOCKET_STATE = False
        elif command == "hearthbeat":
            dataToSend = '{"cmd" : "alive"}'
            sendData(socket_con, dataToSend)
            sendData(socket_con, sendDistance())
        elif command == "robotMovement":
            changeRobotSpeed(dataJson)
        elif command == "cameraMovement":
            changeCameraSpeed(dataJson)
        elif command == "buzz":
            buzz()
        elif command == "manualMode":
            manualMode()
        elif command == "followLine":
            followLine()
        elif command == "autoPilot":
            autoPilot()
        else :
            print("COMMAND DOESNT EXIST")
    else:
        print("NO COMMAND FOUND IN JSON")
    return SOCKET_STATE
        
def changeLedColor(dataJson):
    Led.changeColor(dataJson["state"], dataJson["red"], dataJson["green"], dataJson["blue"])
    
def sendData(socket_con, dataToSend):
    socket_con.send(dataToSend.encode())

def buzz():
    Honk.buzz()

def changeRobotSpeed(dataJson):
    RobotMovement.changeSpeed(dataJson["angle"],dataJson["strength"])
    
def changeCameraSpeed(dataJson):
    CameraMovement.changePosition(dataJson["x"],dataJson["y"])
    
def sendDistance():
    distance = Ultrasonic.getDistance()
    dataJson = '{"cmd" : "distance", "distance" :"' + str(distance) + '"}'
    return dataJson

def followLine():
    RobotMovement.shutdownThreadRobotMovement()
    Tracking.startTracking()

def manualMode():
    Tracking.shutdownThreadFollowLine()
    Autopilot.shutdownThreadAutoPilot()
    
def autoPilot():
    RobotMovement.shutdownThreadRobotMovement()
    Autopilot.startAutoPilot()