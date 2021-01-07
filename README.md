# Raspberrypi 3 Auto Vehicle

The project is a Raspberry Pi based vehicle that implements automatic road tracking,
Bluetooth joystick controlled movement, and obstacle avoidance.

## Usage

```shell
python main.py --help
```

All relevant GPIO pins, vehicle standard speed, vehicle CarStatus, and processing
frequency are defined in [config.py](config.py). It can be modified today to meet other
requirements.

## Hardware

1. Raspberry Pi 3
2. CSI Camera
3. Infrared Sensors
4. Ultrasound Sensors
5. Car Skeleton
6. Four Motors
7. Other Accessories

## Camera and Sensors

### Camera

The camera on the raspberry pi needs to be enabled in advance. Picamera is used to get
data from the camera and process it accordingly. The settings for the camera section are
in [camera.py](plugins/camera.py).

We are using Picamera to get the raw data and process it into jpeg format for web
display.

### Infrared Sensor

The infrared sensors are installed on the left and right front of the vehicle and can be
used to monitor the presence of obstacles in the corresponding direction. The default
value of the sensor is `int`, to make it more readable, it is converted to `bool` and
returned via a `Tuple`. It is defined in [infrared.py](plugins/infrared.py).

### Ultrasound Sensor

Ultrasonic sensors are installed in front of the car and can be used to obtain the
distance between the obstacle and the car. The accuracy is poor for places with more
obstacles. It is defined in [ultrasound.py](plugins/ultrasound.py).

## Automatic Road Tracking

## Bluetooth Gamepad Controlled Movement

The controller provides interaction with the xbox one gamepad to control movement via
the left stick, and RB and LB button provide deceleration and acceleration functions
respectively.

We ara using [xpadneo](https://github.com/atar-axis/xpadneo) to drive the gamepad
and [python-evdev](https://github.com/gvalkov/python-evdev) to read the status of
gamepad. Please follow the guide of xpadneo to connect your gamepad to Raspberry Pi and
adjust setting in [controller.py](plugins/controller.py) to match your gamepad.

## Obstacle Avoidance

Obstacle avoidance is based on ultrasonic sensors and infrared sensors. Motion decisions
are made based on these two data, with the ultrasonic sensor data playing a dominant
judgment role due to the close detection distance of the infrared sensor. The processing
logic is defined in [obstacle_avoid.py](plugins/obstacle_avoid.py).

## Authors

* [guitaoliu](https://github.com/guitaoliu)
* [XDong18](https://github.com/XDong18)
* [merak0514](https://github.com/merak0514)
* [yfc12138](https://github.com/yfc12138)
* [aiueo115](https://github.com/aiueo115)

## License

This project is open sourced under MIT license, see the [LICENSE](LICENSE) file for more
details.
