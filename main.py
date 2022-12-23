from flask import Flask, render_template, request, url_for, flash, redirect
import os
import DataProcess as DP
import pyfirebase as base
import AVRtool as AVR
import time
import threading





# ...
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*32
app.config['SECRET_KEY'] = '1709'
app.config['ALLOWED_EXTENSIONS'] = {'.hex'}
# app.config['SERVER_NAME'] = 'https://esp8266-avrisp.herokuapp.com'


messages = [{'title': 'Debug Terminal',
             'content': 'Below are debug output'},
            {'title': 'TCP/IP',
             'content': '113.172.96.69 : 328'}
            ]

count = 0
debug_log = ''

# ...

TCP_IP =  '113.172.96.69'
TCP_PORT = 328

# ...

@app.route('/')
def index():
    global messages
    time.sleep(1)
    return render_template('index.html', messages=messages)

# ...


class MyWorker():

  def __init__(self, page):
    with app.app_context():
        self.page = page
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

  def run(self):
    with app.app_context():
        global TCP_IP
        global TCP_PORT
        global messages
        start_time = time.time()
        log = AVR.AVR_ISP(TCP_IP,TCP_PORT,self.page)
        messages.append({'title': 'Debug OTA logs', 'content' : ''})
        for i in range(0,len(log),2):
            messages.append({'title': log[i], 'content' : log[i+1]})
        messages.append({'title': 'Execution time:', 'content' : time.time() - start_time})
        # return redirect(url_for("upload"))

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
        global TCP_IP
        global TCP_PORT
        global count
        # try:
        file = request.files['uploadfile']
        AVR_type = request.form['F_type']
        if AVR_type == "Custom":
            IP = request.form['TCP']
            Port = request.form['Port']
            if not IP:
                IP = TCP_IP
            elif not Port:
                Port = TCP_PORT
            else:
                TCP_IP = IP
                TCP_PORT = int(Port)
        if AVR_type == "Default":
            TCP_IP =  '113.172.96.69'
            TCP_PORT = 328
        messages[1]['content'] = TCP_IP + ' : ' + str(TCP_PORT)
        count += 1
        extension = os.path.splitext(file.filename)[1]
        # realpath = os.path.realpath(file.filename)
        Block = []
        if file:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'Not a hex file'
            for line in file.readlines():
                Block.append(str(line.rstrip()))
                
            page = DP.convert_hex_file(Block)
            MyWorker(page)
            messages.append({   'title': 'OTA state no.'+str(count),
                                'content' : 'The program OTA is running in the background, please wait for a minutes'})
            return redirect(url_for('index'))
        # except:
        #     return 'Not allowed.'
        
    return render_template('upload.html')