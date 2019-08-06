from flask import Flask, request
import numpy as np
import cv2
import json
import base64

app = Flask(__name__)

@app.before_first_request
def startup():
    global face_cascade
    face_cascade = cv2.CascadeClassifier('cascade.xml')

@app.route("/detect", methods=['POST'])
def detect():
    global face_cascade

    req_json = request.get_json()
    if 'content' in req_json:
        np_img = np.fromstring(base64.b64decode(req_json['content']), np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        faces = face_cascade.detectMultiScale(gray, 
                                            scaleFactor = 1.1, 
                                            minNeighbors = 5, 
                                            minSize = (24, 24))

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        cv2.imwrite("res_img.png", img)

        _, buffer = cv2.imencode('.jpg', img)
        jpg_as_text = base64.b64encode(buffer)
        return json.dumps({"content": jpg_as_text.decode("utf-8")})

    return json.dumps({"success": False})

if __name__ == "__main__":
    app.run()