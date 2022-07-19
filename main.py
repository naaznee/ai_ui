from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)

alert_error_template = '<div class="alert alert-danger" role="alert">Choose some files to upload!</div>'
alert_success_template = '<div class="alert alert-success" role="alert">Files uploaded successfully</div>'

gender_dict = {0:'Male', 1:'Female'}
race_dict={0:'White', 1:'Black',2:'Asian',3:'Indian',4:'Others (like Hispanic, Latino, Middle Eastern)'}

MODEL = None

def load_model(path):
    import tensorflow as tf
    global MODEL
    if not MODEL:
        MODEL = tf.keras.models.load_model(path)
    return MODEL

def load_process_model(image):
    from keras.utils.image_utils import load_img
    from PIL import Image
    import numpy as np

    model = load_model("models/saved_model.h5")

    with open(image, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    
    img = load_img(image, color_mode = "grayscale")
    img = img.resize((128, 128), Image.ANTIALIAS)
    img = np.array(img)

    pred = model.predict(img.reshape(1, 128, 128, 1))
    pred_gender = gender_dict[round(pred[0][0][0])]
    pred_age = round(pred[1][0][0])

    return {
        "gender": pred_gender,
        "age": pred_age,
        "race": "blah",
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
        dst = f"/tmp/{sec_filename}"
        _file.save(dst)
        preds[sec_filename] = load_process_model(dst)
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
