import socket
import struct
import threading

DEADZONE = 0.05
class OI:

    def __init__(self):
        thread = threading.Thread(target=self.threadRoutine).start()
        self.LJoystickXAxisRaw = 127
        self.LJoystickYAxisRaw = 127
        self.RJoystickXAxisRaw = 127
        self.RJoystickYAxisRaw = 127
        self.AButtonRaw = 0
        self.BButtonRaw = 0
        self.XButtonRaw = 0
        self.YButtonRaw = 0
        self.StartButtonRaw = 0
        self.LeftBumperRaw = 0
        self.RightBumperRaw = 0
        self.RightTriggerAxisRaw = 127
        self.LeftTriggerAxisRaw = 127
        self.data = 0

    def threadRoutine(self):
        # Define the IP address and port number to listen on
        ip_address = "0.0.0.0"
        port = 4143

        # Create a TCP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the IP address and port
        s.bind((ip_address, port))

        # Listen for incoming connections
        s.listen()

        # Accept a connection
        conn, addr = s.accept()

        while True:
            # Receive data
            dataRaw = conn.recv(1024)
            data = bytearray(dataRaw)
            self.LJoystickXAxisRaw = data[0]
            self.LJoystickYAxisRaw = data[1]
            self.RJoystickXAxisRaw = data[2]
            self.RJoystickYAxisRaw = data[3]
            self.AButtonRaw = data[4]
            self.BButtonRaw = data[5]
            self.XButtonRaw = data[6]
            self.YButtonRaw = data[7]
            self.StartButtonRaw = data[8]
            self.LeftBumperRaw = data[9]
            self.RightBumperRaw = data[10]
            self.RightTriggerAxisRaw = data[11]
            self.LeftTriggerAxisRaw = data[12]

        # Close the connection
        conn.close()

    def getLeftJoystickXAxis(self):
        value = ((self.LJoystickXAxisRaw - 127.0) / 127.0)
        if abs(value) > DEADZONE:
            return value
        else:
            return 0

    def getLeftJoystickYAxis(self):
        value = ((self.LJoystickYAxisRaw - 127.0) / 127.0)
        if abs(value) > DEADZONE:
            return value
        else:
            return 0

    def getRightJoystickXAxis(self):
        value = ((self.RJoystickXAxisRaw - 127.0) / 127.0)
        if abs(value) > DEADZONE:
            return value
        else:
            return 0

    def getRightJoystickYAxis(self):
        value = ((self.RJoystickYAxisRaw - 127.0) / 127.0)
        if abs(value) > DEADZONE:
            return value
        else:
            return 0

    def getAButtonPressed(self):
        return self.AButtonRaw

    def getBButtonPressed(self):
        return self.BButtonRaw

    def getXButtonPressed(self):
        return self.XButtonRaw

    def getYButtonPressed(self):
        return self.YButtonRaw

    def getStartButtonPressed(self):
        return self.StartButtonRaw

    def getLeftBumperPressed(self): 
        return self.LeftBumperRaw

    def getRightBumperPressed(self):
        return self.RightBumperRaw

    def getRightTriggerAxis(self):
        value = ((self.RightTriggerAxisRaw - 127.0) / 127.0)
        if abs(value) > DEADZONE:
            return value
        else:
            return 0        

    def getLeftTriggerAxis(self):
        value = ((self.LeftTriggerAxisRaw - 127.0) / 127.0)
        if abs(value) > DEADZONE:
            return value
        else:
            return 0
        

