import logging
from threading import Thread

from web import app

logger = logging.getLogger(__name__)


def main():
    Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port="8080",
            debug=False,
            threaded=True,
        )
    ).start()


if __name__ == "__main__":
    main()
