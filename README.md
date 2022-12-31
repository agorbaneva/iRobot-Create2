# iRobot Create2 GUI with Live Video Object Detection using CNNs, YOLOv5

A GUI for controlling the [iRobot Create 2 Robot](https://www.irobot.com/en_US/irobot-create-2-programmable-robot/RC65099.html) coded in Python with PyQt5. Once the robot establishes a connection with the GUI via a mini-DIN to USB cable, the robot moves with WASD controls. The robot can follow a drawn path on the GUI and return to its dock to recharge with a button press.

The GUI shows the robot's battery level and wirelessly displays live video from a Raspberry Pi's Camera Module V2.

In real time, the robot analyzes the video feed for objects using YOLOv5. Specifically, the robot detects pigeons with a 0.9 confidence level, but any YOLOv5 trained model's weights can be swapped out in the YOLOv5 folder to detect other objects.

<p align="center">
  <img src="https://user-images.githubusercontent.com/74417274/210126009-b2d3489b-b052-49ae-9dc0-20a0394a9cc7.png">
</p>

## Robot Implementation

* Run `main.py` to launch the GUI.
* Click the upper left dropdown to establish a connection with the robot (at the correct USB port). Battery should automatically update.
* Switch the iRobot between "Passive" and "Safe" (able to be programmable) modes using the other menu buttons. WASD controls and path-drawing controls activate in Safe mode.
* Click "return to base" to send the robot back to its charging station.

## Object Detection and Live Camera Feed

* Ensure that the Raspberry Pi and computer running the GUI are connected to the same Wi-Fi network. Add the IP address to both `client.py` and in `WorkerThreads.py` files.
* Download the `client.py` file to your Raspberry Pi to establish a socket connection.
* Run the GUI. Live video should display. Click "Capture Image" to freeze at a particular image.
* Uncomment the torch model code if you would like to have object detection run simulataneously. Warning for slower video feed.

![](https://user-images.githubusercontent.com/74417274/204418784-378abc71-2ba4-4525-a52f-86d5ff716e3b.png)

Created with funding from the TJHSST Computer Systems Research Lab.
