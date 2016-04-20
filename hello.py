import os, io
import random
from flask import Flask, request, jsonify, send_file, abort, render_template
from werkzeug import secure_filename
import numpy as np
import cv2
import glcm
import ml

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif', 'tif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    return render_template('index.html')

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

def normalize(x, i):
    maxf = [1.0, 6.19758064516129, 1.5604838709677413, 0.98588709677419351, 0.68681914997398541, 2.1254609840386753, 29.664314516129032, 41.667055953677796, 0.99037925143216643]
    minf = [1.0, 0.028225806451612906, 0.028225806451612906, 0.47708894582268951, 0.010091823296045778, 0.33620654547412704, 6.9576612903225818, 0.10627738643015089, 0.29237699071068468]
    return ((x-minf[i])/(maxf[i]-minf[i]))*2-1

@app.route("/upload", methods=['POST'])
def upload():
    photo = request.files.get('image', '')
    if photo:
        filename = secure_filename(photo.filename)
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, 0) # 0 flag for grayscale
        result = glcm.get_features(img)
        X = [1, normalize(result['contrast'], 1), normalize(result['dissimilarity'], 2),
            normalize(result['homogeneity'], 3), normalize(result['ASM'], 4),
            normalize(result['entropy'], 5), normalize(result['GLCM_mean_i'], 6),
            normalize(result['GLCM_variance_i'], 7), normalize(result['GLCM_correlation'], 8)]
        answer = ml.get_result(X)
        return jsonify({"result": 1-answer})
    else:
        abort(404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

# and allowed_file(file.filename)
