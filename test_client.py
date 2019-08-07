import requests
import json
import numpy as np
import cv2
import base64

addr = 'http://localhost:5000'
test_url = addr + '/auto_crop'

# HTTP request headers
content_type = 'application/json'
headers = {'content-type': content_type}

# Read and encode image as jpeg
img = cv2.imread('Training/show_img/1.png')
_, buffer = cv2.imencode('.jpg', img)
jpg_as_text = base64.b64encode(buffer)

# Send request, decode response
response = requests.post(test_url, json={"content": jpg_as_text.decode("utf-8")}, headers=headers)

res_json = json.loads(response.text)
#print(res_json)

# Decode base64-encoded response image
encoding = res_json['image']
np_img = np.fromstring(base64.b64decode(encoding), np.uint8)
img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
cv2.imshow('response', img)
cv2.waitKey(0)
cv2.destroyAllWindows()