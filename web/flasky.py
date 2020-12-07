from flask import Flask, Response, render_template

from plugins.camera import Camera

app = Flask(__name__, template_folder="./templates")
camera = Camera()


@app.route("/")
def index():
    return render_template("index.html")


def gen(camera: Camera):
    while True:
        frame = camera.get_frame()
        yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


def gen_detected(camera: Camera):
    while True:
        frame = camera.get_detected_frame()
        yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"


@app.route("/detectResult")
def detect_result():
    return Response(gen_detected(camera), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/cameraStream")
def camera_stream():
    return Response(gen(camera), mimetype="multipart/x-mixed-replace; boundary=frame")
