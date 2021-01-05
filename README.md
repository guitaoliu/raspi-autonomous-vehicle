# Raspberrypi 3 Auto Vehicle

The project is a Raspberry Pi based vehicle that implements automatic road tracking, Bluetooth joystick controlled movement, and obstacle avoidance.

## Usage

```shell
python main.py --help
```

## Hardware

## Camera and Sensors

## Automatic Road Tracking

## Bluetooth Gamepad Controlled Movement

The controller provides interaction with the xbox one gamepad to control movement via the left stick, and RB and LB button provide deceleration and acceleration functions respectively.

We ara using [xpadneo](https://github.com/atar-axis/xpadneo) to drive the gamepad and [python-evdev](https://github.com/gvalkov/python-evdev) to read the status of gamepad. Please follow the guide of xpadneo to connect your gamepad to Raspberry Pi and adjust setting in [controller.py](plugins/controller.py) to match your gamepad.

## Obstacle Avoidance

## Authors

* [guitaoliu](https://github.com/guitaoliu)
* [XDong18](https://github.com/XDong18)
* [merak0514](https://github.com/merak0514)
* [yfc12138](https://github.com/yfc12138)
* [aiueo115](https://github.com/aiueo115)

## License

This project is open sourced under MIT license, see the [LICENSE](LICENSE) file for more details.
