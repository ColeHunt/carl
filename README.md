# CySAR - CARL
## Description
Certified. Autonomous. (with) Robotic. Legs.
CARL is the current robot in development by the M2I CySAR team. This repo is for the onboard software for the robot to be run on the Jetson.

The robot consists of 4 flippers with treads to allow multi terrain navigation. The robot operates in an arcade drive manner. This means driving is mapped to one joystick with the Y-Axis as Speed and the X-Axis as Steering. The flippers are controlled independently to allow for maximum flexibility and are position based.

## Connecting to the Robot (Ethernet)
1. Connect an ethernet cable between your host machine and the Jetson
2. Open a Terminal or Serial Connection Program of your choosing. (Powershell, Putty, etc)
3. Run `ssh cysar@cysar.local` in the terminal
    - You will be asked for a password: `cysarpw` (password will be invisible)
    - If this is your first time connecting you will be prompted if you would like to ask your device to a list of know hosts. Select yes by typing `y`

## Connecting to the Robot (Wifi)
1. Connect the host machine to the IASTATE network
2. Open a Terminal or Serial Connection Program of your choosing. (Powershell, Putty, etc)
3. Run `ssh cysar@2610:130:110:1525:47e7:9414:7e67:15e4` in the terminal
    - You will be asked for a password: `cysarpw` (password will be invisible)
    - If this is your first time connecting you will be prompted if you would like to ask your device to a list of know hosts. Select yes by typing `y`

## CANable Setup
The robot runs of Rev Spark Max motorcontrollers all of which are controlled of the CAN bus. The Jetson communicates over CAN using the CANable USB Adapter. The repo includes a script to setup the CANable *can0setup.sh*. This script **must** be run in a Linux enviroment and will **not** work in a Windows enviroment.

#### can0 Interface Setup
1. Open a terminal and navigate to the project directory
    - [Shell Navigation Commands](https://www.guru99.com/linux-commands-cheat-sheet.html)
2. Plug the CANable into a USB port on the driving device (Jetson or Linux Machine)
3. Run the script as superuser using `sudo can0setup.sh` in the terminal
    - If you are running this script on a PC and **not** the Jetson you will need to include the a `pc` arg on the command ie `sudo ./can0setup.sh pc`
4. You can confirm the `can0` interface is setup by running `ifconfig` in the terminal. You will see a list of configured interface on your machine one of which should be named `can0`

```
can0: flags=193<UP,RUNNING,NOARP>  mtu 16
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
        RX packets 16  bytes 128 (128.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1  bytes 4 (4.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

#### Adapter Testing
(This step is not necessary to start robot)
The adapter should be setup on the system and can be tested by doing the following
1. Open a new termianl and run `candump can0`
    - This should show all traffic received by can0. The terminal will be blocked while the candump is running while waiting for messages
2. Then in a different terminal run `cansend can0 999#DEADBEEF`
    - This will send a frame to `0x999` with payload `0xdeadbeef` and you should see the message appear in the candump terminal
    ```
    can0  199   [4]  DE AD BE EF
    ```
3. After this test ensure to close the candump terminal using `Ctrl-C` to ensure the machine is not reading all CAN messages to the robot.

## Teleop Control
The primary or *main* file of the program is `teleop.py`. This file is setup to be an executable that will run the primary control loop for the robot.

#### Enabling the Robot
To start the primary control loop the following steps need to be complete. Before you begin ensure you have ***connected to the robot*** and that the ***`can0` interface is setup***.

**WARNING: These steps do not include any of the required actions to power on the robot. Please consult the System Team Checklist for Robot Opertaion and Configuration**
1. Confirm that the CANable is connected to the driver device and that the CAN bus end has been attached to the robot CAN bus.
2. The Robot **must** be turned **on** to proceed with further instructions.
    - If the Robot in not powered on the CANable will attempt to to read and recieve data and cause a buffer overflow.

**WARNING: Once the next step is run the robot will be live and will attempt to react to Joystick inputs. Do not continue if this not desired**

3. The robot can now be enabled by running `teleop.py`
    - The program will wait for a controller to be detect and then begin to send CAN messages to the robot executing the desired actions
4. To start recieving controller inputs you will need to start the `baseStation` on a seperate device
    - See [baseStation](https://github.com/M2I-CYSAR/baseStation#readme) for further details
