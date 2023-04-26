import socket
import struct
import threading

# Set Flag for Robot system Enable
ENABLED = True

CMD = 0
CONTROL = 1

DEADZONE = 0.05
class OI:

    def __init__(self):
        thread = threading.Thread(target=self.threadRoutine).start()
        self.LJoystickXAxisRaw = 0
        self.LJoystickYAxisRaw = 0
        self.AButtonRaw = 0
        self.BButtonRaw = 0
        self.Enabled = False

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

            if (data[0] == CMD):
                self.Enabled = data[1]

            if (data[1] == CONTROL):
                self.LJoystickXAxisRaw = data[1]
                self.LJoystickYAxisRaw = data[2]
                self.AButtonRaw = data[3]
                self.BButtonRaw = data[4]


        # Close the connection
        conn.close()

    def isEnabled(self):
        return self.Enabled

    def getLeftJoystickXAxis(self):
        if self.LJoystickXAxisRaw > DEADZONE:
            return ((self.LJoystickXAxisRaw - 127.0) / 127.0)
        else:
            return 0

    def getLeftJoystickYAxis(self):
        if self.LJoystickYAxisRaw > DEADZONE:
            return ((self.LJoystickYAxisRaw - 127.0) / 127.0)
        else:
            return 0

    def getAButtonPressed(self):
        return self.AButtonRaw

    def getBButtonPressed(self):
        return self.BButtonRaw

