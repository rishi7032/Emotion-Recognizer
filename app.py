from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

class VideoCamera:
    def __init__(self):
        # Open the default camera (you can change the index or camera device path based on your setup)
        self.video_capture = cv2.VideoCapture(0)

    def __del__(self):
        self.video_capture.release()

    def get_frame(self):
        success, frame = self.video_capture.read()
        if not success:
            return None

        # Perform any additional image processing here if needed
        # For example, you can use OpenCV functions like cv2.cvtColor, cv2.resize, etc.

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

def generate(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/video")
def video():
    return render_template("video.html")

if __name__ == '__main__':
    app.run(debug=True)
