from flask import Flask, Response, render_template

from core import car

app = Flask(__name__, template_folder="./templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cameraStream")
def camera_stream():
    def gen():
        while True:
            frame = car.camera.frame.tostring()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/grayStream")
def gray_stream():
    def gen():
        while True:
            frame = car.track.jpeg.tostring()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")
