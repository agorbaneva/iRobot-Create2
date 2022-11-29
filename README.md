# iRobot Create2 GUI with Live Video Object Detection using CNNs, YOLOv5

A GUI for controlling the [iRobot Create 2 Robot](https://www.irobot.com/en_US/irobot-create-2-programmable-robot/RC65099.html) coded in Python with PyQt5. Once the robot establishes a connection with the GUI via a mini-DIN to USB cable, the robot moves with WASD controls. The robot can follow a drawn path on the GUI and return to its dock to recharge with a button press.

The GUI shows the robot's battery level and wirelessly displays live video from a Raspberry Pi's Camera Module V2.

In real time, the robot analyzes the video feed for objects using YOLOv5. Specifically, the robot detects pigeons with a 0.9 confidence level, but any YOLOv5 trained model's weights can be swapped out in the YOLOv5 folder to detect other objects.

![](https://user-images.githubusercontent.com/74417274/204418784-378abc71-2ba4-4525-a52f-86d5ff716e3b.png)
