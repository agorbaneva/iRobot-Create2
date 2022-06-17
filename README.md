# iRobot-Create2-Programmable-Robot-GUI-Using-YOLOv5

A GUI for controlling the [iRobot Create 2 Programmable Robot](https://www.irobot.com/en_US/irobot-create-2-programmable-robot/RC65099.html) coded in Python with PyQt5. Once the robot establishes a connection with the GUI via a mini-DIN to USB cable, the robot moves with WASD controls, and the GUI displays the robot's battery level. The robot can follow a drawn path on the GUI, return to its dock to recharge with a button press, and wirelessly display live video from a Raspberry Pi's Camera Module V2.

In real time, the robot analyzes the video feed for objects using YOLOv5. Specifically, the robot detects pigeons with a 0.9 confidence level, but any YOLOv5 trained model's weights can be swapped out in the YOLOv5 folder to detect other objects.
