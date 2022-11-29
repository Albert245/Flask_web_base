from flask import Flask, render_template, request, url_for, flash, redirect
import os
import DataProcess as DP
import pyfirebase as base
import ntpath




# ...
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*32
app.config['SECRET_KEY'] = 'your secret key'
app.config['ALLOWED_EXTENSIONS'] = {'.hex'}


messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]
# ...

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

# ...

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/upload', methods = ('GET','POST'))
def upload():
    if request.method == 'POST':
        try:
            file = request.files['uploadfile']
            file_base_name = os.path.basename(file.filename)
            extension = os.path.splitext(file.filename)[1]
            filename = os.path.splitext(file.filename)[0]
            Block = []
            if file:
                if extension not in app.config['ALLOWED_EXTENSIONS']:
                    return 'Not a hex file'
                for line in file.readlines():
                    Block.append(str(line.rstrip()))
                    
                page = DP.convert_hex_file(Block)
                base.upload(file_base_name)
                return file_base_name
        except:
            return 'Not allowed'
    return render_template('upload.html')
