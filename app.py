import os

from flask import Flask, render_template, request,redirect

from ocr_core import ocr_core
from gtts import gTTS


AUDIO_FOLDER = '/static/audio/'
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/proceed', methods=["GET","POST"])
def proceed():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
       return redirect("upload.html")

@app.route('/preview', methods=['GET', 'POST'])
def preview_page():
    if request.method == 'POST':
        file = request.files['file']
        lang = request.form['lang']
        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            extracted_text = ocr_core(file,lang)
            # extract the text and display it
            return render_template('preview.html', language=lang , msg='Successfully Uploaded',img_src=UPLOAD_FOLDER + file.filename,extracted_text=extracted_text)
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/aud', methods=['GET', 'POST'])
def aud():
    text = request.form['text']
    language = request.form['language']  # voice language set to English.

    speech = gTTS(text=text, lang=language[:2])     # slow=False
    path=os.path.join(os.getcwd() + AUDIO_FOLDER, "text.mp3")
    speech.save(path)  # text file to mp3 conversion.
    return render_template('audio_page.html',aud_src=AUDIO_FOLDER + "text.mp3")

def loading():
    file = request.files['file']
    return render_template('loading.html',file=file)

@app.route('/success', methods=['GET', 'POST'])
def success():
    file = request.files['file']
    extracted_text = ocr_core(file)
    return render_template('success.html',msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)

if __name__ == '__main__':
    app.run()

