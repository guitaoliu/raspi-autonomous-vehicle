import time


from web import app
from plugins.motor import test_motor


def main():
    app.run(
        host='0.0.0.0',
        port='8080',
        debug=True,
        threaded=True
    )
    test_motor()


if __name__ == "__main__":
    main()
