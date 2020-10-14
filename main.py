
from web import app


def main():
    app.run(
        host='0.0.0.0',
        port='8080',
        debug=True,
        threaded=True
    )

if __name__ == "__main__":
    main()
