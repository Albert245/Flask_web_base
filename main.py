from flask import Flask, render_template, request, url_for, flash, redirect
import os
import numpy as np

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
            extension = os.path.splitext(file.filename)[1]
            Block = []
            if file:
                if extension not in app.config['ALLOWED_EXTENSIONS']:
                    return 'Not a hex file'
                for line in file.readlines():
                    Block.append(str(line.rstrip()))
                    
                page = extractData(11,-3,Block)
                return page
        except:
            return 'Not allowed'
    return render_template('upload.html')

def extractData(start,stop, raw_data):
    data = []
    for i in range(len(raw_data)):
        a = raw_data[i]
        if len(a)>12:
            data.append(a[start:stop])
    while("" in data):
        data.remove("")
    listdata = list2D(data)
    return listdata

def String_split_nth(str_line,n):
    return [str_line[i:i+n] for i in range(0,len(str_line),n)]

def list2D(list):
    list_out = []
    for i in range(0,len(list)):
        list_out.append(String_split_nth(list[i],2))
    return list_out
