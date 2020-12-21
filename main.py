import logging
from threading import Thread

from core import Car
from web import app

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port="8080",
            debug=False,
            threaded=True,
        )
    ).start()
    with Car() as c:
        while True:
            c.update(c.status.FORWARD_FAST)


if __name__ == "__main__":
    main()
