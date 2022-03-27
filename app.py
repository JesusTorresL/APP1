from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os
from gtts import gTTS
from playsound import playsound

if os.environ.get('DOCKER', '') == "yes":
    UPLOAD_FOLDER = '/usr/src/app/images'
else:   
    UPLOAD_FOLDER = 'images'

UPLOAD_FOLDER = "images"

ALLOWED_EXTENSIONS =set(['txt','pdf','png','jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    NO_VALID_IMAGE = "No se ha proporcionado un imagen valida."
    if request.method == 'POST' and request.files:
        f = request.files['image']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        img =Image.open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
        try:
            text=pytesseract.image_to_string(img, "spa")
        except Exception as e:
            return render_template('results.html', text=NO_VALID_IMAGE)
        if not os.environ.get('DOCKER', '') == "yes":
            myobj=gTTS(text=text, lang='es', slow = False)
            myobj.save(app.config['UPLOAD_FOLDER'] + "/speech.mp3")
            playsound(app.config['UPLOAD_FOLDER'] + "/speech.mp3")

        return render_template('results.html', text=text)
    
    return render_template('home.html', text=NO_VALID_IMAGE)

if __name__=="__main__":
    app.run(debug = True)