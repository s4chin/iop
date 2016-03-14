import os
from flask import Flask, request, jsonify
from werkzeug import secure_filename

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    return "Hello, world!"



@app.route("/upload", methods=['POST'])
def upload():
    file = request.files.get('image', '')
    if file:
        filename = secure_filename(file.filename)
        return jsonify(result=0.598)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# and allowed_file(file.filename)
