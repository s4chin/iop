import os, io
import random
from flask import Flask, request, jsonify, send_file, abort
from werkzeug import secure_filename
import numpy as np
import cv2
import glcm

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'tif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    return "Hello, world!"

@app.route("/extract", methods=['POST'])
def extract():
    photo = request.files.get('image', '')
    if photo:
        filename = secure_filename(photo.filename)
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, 0) # 0 flag for grayscale
        result = glcm.get_features(img)
        return jsonify(result)
    else:
        abort(404)

# @app.route("/segment", methods=['POST'])
# def segment():
#     photo = request.files.get('image', '')
#     if photo:
#         filename = secure_filename(photo.filename)
#         #return send_file('python.png', mimetype='image/png')
#         in_memory_file = io.BytesIO()
#         photo.save(in_memory_file)
#         data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
#         color_image_flag = 1
#         img = cv2.imdecode(data, 0) # 0 flag for grayscale
#         ret, jpg = cv2.imencode('.jpg', img)
#         jpg = jpg.tobytes()
#         return send_file(io.BytesIO(jpg),
#                          attachment_filename='image.jpg',
#                          mimetype='image/jpg')
# 
#     else:
#         abort(404)

@app.route("/upload", methods=['POST'])
def upload():
    photo = request.files.get('image', '')
    if photo:
        filename = secure_filename(photo.filename)
        return jsonify({"result": random.random()})
    else:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# and allowed_file(file.filename)
