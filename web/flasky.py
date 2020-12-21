from flask import Flask, Response, render_template

from sensors.camera import Camera

app = Flask(__name__, template_folder="./templates")
camera = Camera()


@app.route("/")
def index():
    return render_template("index.html")


def gen():
    with camera as ca:
        while True:
            frame = ca.frame.tostring()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


@app.route("/cameraStream")
def camera_stream():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")
