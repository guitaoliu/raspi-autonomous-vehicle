from flask import Flask, Response, jsonify, render_template, request
from flask_cors import CORS

from core import car

app = Flask(__name__, template_folder="./templates", static_folder="./static")
CORS(app, supports_credentials=True, resources=r"/*")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cameraStream")
def camera_stream():
    source_type = request.args.get("type", default="plain", type=str)

    def gen():
        while True:
            if source_type == "plain":
                frame = car.camera.frame.tostring()
            elif source_type == "twoLine":
                frame = car.track.jpeg
            else:
                frame = car.camera.frame.tostring()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/carStatus")
def car_status():
    obstacle_status = car.obstacle()
    distance_data = car.distance()
    status = str(car.status)
    return jsonify(
        {
            "left": obstacle_status[0],
            "right": obstacle_status[1],
            "status": status,
            "distance": distance_data,
        }
    )
