from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f'uploads/{file.filename}')
    return redirect('/')