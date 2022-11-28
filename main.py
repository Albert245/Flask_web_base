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
                    
                page = fill(Datafile2hex(Block))
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
    return data

#Split string into nth
def String_split_nth(str_line,n):
    list_splited = [str_line[i:i+n] for i in range(0,len(str_line),n)] #Split done here
    for i in range(len(list_splited)):
        list_splited[i] = hex(int(list_splited[i],16))  # turn list of strings to list of hex one-by-one
    return list_splited



def list2Dhex(list):
    list_out = []
    for i in range(0,len(list)):
        list_out.append(String_split_nth(list[i],2))
    combine = compress_list(list_out)
    return combine

#  turn Datafile into 2D-list of hex
def Datafile2hex(Data_list): 
    Data_extracted = list2Dhex(extractData(11,-3,Data_list))
    return Data_extracted

# compress list of list to 1 list
def compress_list(list):
    compress = []
    for i in range(len(list)):
        compress += list[i]
    return compress

# fill list to 128 per
def fill(list):
    filled_list = []
    idx = 0
    for i in range(len(list)):
        filled_list.append(list[i])
        idx += 1
    while idx % 128 != 0:
        filled_list.append(hex(255))
        idx+=1
    return filled_list



# turn list to numpy Block[n]
def Convert2Block(list,n):
    return np.reshape(np.array(list),(len(list)//n,n))

# convert hex list to numpy Block can use for flashing
def convert_hex_file(list):
    return Convert2Block(fill(Datafile2hex(list)),128)