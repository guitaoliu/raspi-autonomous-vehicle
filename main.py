import argparse
import logging
from threading import Thread

import RPi.GPIO as GPIO

from core import car
from web import app

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def load_parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--method",
        type=str,
        default="two_line",
        choices=["two_line_track", "obstacle_avoid"],
        help="Car running method",
    )
    parser.add_argument("-w", "--web", action="store_true")
    return parser


def main():
    args = load_parse().parse_args()
    if args.web:
        Thread(
            target=lambda: app.run(
                host="0.0.0.0",
                port="8080",
                debug=False,
                threaded=True,
            )
        ).start()
    logger.info(f"Start car with {' '.join(args.method.split('_'))}")
    with car as c:
        try:
            c.run(method=args.method)
        except KeyboardInterrupt:
            c.camera.close()
            GPIO.cleanup()


if __name__ == "__main__":
    main()
