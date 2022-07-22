import base64
import hashlib
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

alert_error_template = '<div class="alert alert-danger" role="alert">Choose some files to upload!</div>'
alert_success_template = '<div class="alert alert-success" role="alert">Files uploaded successfully</div>'

gender_dict = {0:'Male', 1:'Female'}
race_dict={0:'White', 1:'Black',2:'Asian',3:'Indian',4:'Others (like Hispanic, Latino, Middle Eastern)'}

model_filemap = {
    "gender":"models/saved_model_20Jul2022_01.h5",
    "age": "models/saved_model_20Jul2022_01.h5",
    "race": "models/saved_model_21Jul2022_race_02.h5"
}

MODELS = {}

def load_model(path):
    import tensorflow as tf
    global MODELS
    if not path in MODELS:
        MODELS[path] = tf.keras.models.load_model(path)
    return MODELS[path]

def verify(image, pred_gender, pred_age, pred_race):
    ## enable for verification
    # temp = os.path.basename(image).split('_')
    # pred_gender= gender_dict[int(temp[1])]
    # pred_age = int(temp[0])
    # pred_race= race_dict[int(temp[2])]
    return {
        "gender": pred_gender,
        "age": pred_age,
        "race": pred_race
    }

def load_process_model(image):
    import numpy as np
    from keras.utils.image_utils import load_img
    from PIL import Image

    with open(image, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')

    img = load_img(image, color_mode = "grayscale")
    img = img.resize((128, 128), Image.ANTIALIAS)
    img = np.array(img)
    img_reshape = img.reshape(1, 128, 128, 1)

    model_01 = load_model(model_filemap.get("gender"))
    pred_01 = model_01.predict(img_reshape)

    pred_gender = gender_dict[round(pred_01[0][0][0])]

    model_02 = load_model(model_filemap.get("age"))
    pred_02 = model_02.predict(img_reshape)
    pred_age = round(pred_02[1][0][0])

    model_03 = load_model(model_filemap.get("race"))
    pred_03 = model_03.predict(img_reshape)
    pred_race = race_dict[list(pred_03[0][0]).index(np.max(pred_03[0][0]))]

    _verify = verify(image, pred_gender, pred_age, pred_race)

    return {
        "gender": _verify["gender"],
        "age": _verify["age"],
        "race": _verify["race"],
        "base64image": b64_string
    }


@app.route("/upload", methods = ['GET', 'POST'])
def upload():
    if not request.method == 'POST':
        return render_template("home.html", alert=alert_error_template)

    files = request.files.to_dict(flat=False).get("file[]")
    valid_files = [_file for _file in files if _file.filename]
    if not valid_files:
        return render_template("home.html", alert=alert_error_template)

    preds = {}
    for _file in files:
        sec_filename = secure_filename(_file.filename)
        file_hash = hashlib.md5(sec_filename.encode()).hexdigest()
        dst = f"/tmp/{sec_filename}"
        _file.save(dst)
        preds[file_hash] = load_process_model(dst)
        os.remove(dst)
    return render_template("home.html", alert=alert_success_template, preds=preds)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
