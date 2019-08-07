from flask import Flask, request, abort
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

        detected = []
        for (x,y,w,h) in faces:
            detected.append({ "x" : int(x), "y" : int(y), "w" : int(w), "h" : int(h) })
        
        print(detected)
        return json.dumps({ "detected" : detected})
    else:
        abort(400, "Invalid request for /detect")


@app.route("/auto_crop", methods=['POST'])
def auto_crop():
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

        print(faces)
        faces = faces.tolist()
        if len(faces):
            max_face_ind = faces.index(max(faces, key=lambda x: x[2]*x[3]))
            x,y,w,h = faces[max_face_ind]
            cropped = img[y:y+h, x:x+w]
        else:
            cropped = img

        cv2.imwrite("res_img.png", cropped)

        _, buffer = cv2.imencode('.jpg', cropped)
        jpg_as_text = base64.b64encode(buffer)
        return json.dumps({"image": jpg_as_text.decode("utf-8")})
    else:
        abort(400, "Invalid request for /auto_crop")

if __name__ == "__main__":
    app.run()