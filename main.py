from flask import Flask, render_template, request, url_for, flash, redirect
import os
import DataProcess as DP
import pyfirebase as base
import AVRtool as AVR
import time
import threading
from flask_socketio import SocketIO
import redis
from rq import Worker, Queue, Connection
#====
import requests




# ...
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*32
app.config['SECRET_KEY'] = '1709'
app.config['ALLOWED_EXTENSIONS'] = {'.hex'}
app.config['SERVER_NAME'] = 'esp8266-avrisp.herokuapp.com'


messages = [{'title': 'Debug Terminal',
             'content': 'Below are debug output'},
            {'title': 'TCP/IP',
             'content': '113.172.96.69 : 328'}
            ]

debug_log = ''

# ...

TCP_IP =  '113.172.96.69'
TCP_PORT = 328
page = []
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
        global TCP_IP
        global TCP_PORT
        try:
            file = request.files['uploadfile']
            IP = request.form['TCP']
            Port = request.form['Port']
            AVR_type = request.form['F_type']
            if AVR_type == "Custom":
                if not IP:
                    IP = TCP_IP
                elif not Port:
                    Port = TCP_PORT
                else:
                    TCP_IP = IP
                    TCP_PORT = Port
            if AVR_type == "Default":
                TCP_IP =  '113.172.96.69'
                TCP_PORT = 328
            messages[1]['content'] = TCP_IP + ' : ' + str(TCP_PORT)
            extension = os.path.splitext(file.filename)[1]
            # realpath = os.path.realpath(file.filename)
            Block = []
            if file:
                if extension not in app.config['ALLOWED_EXTENSIONS']:
                    return 'Not a hex file'
                for line in file.readlines():
                    Block.append(str(line.rstrip()))
                global page
                page = DP.convert_hex_file(Block)
                # MyWorker(page)
                q = Queue(connection=conn)
                result = q.enqueue(task, 'esp8266-avrisp.herokuapp.com')
                return 'Loading'
        except:
            return 'Not allowed'
        
    return render_template('upload.html')

class MyWorker():

  def __init__(self, page):
    with app.app_context():
        self.page = page
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()
        thread.join()
        return redirect("esp8266-avrisp.herokuapp.com")

  def run(self):
    with app.app_context():
        global TCP_IP
        global TCP_PORT
        global messages
        start_time = time.time()
        log = AVR.AVR_ISP(TCP_IP,TCP_PORT,self.page)
        for i in range(0,len(log),2):
            messages.append({'title': log[i], 'content' : log[i+1]})
        messages.append({'title': 'Execution time:', 'content' : time.time() - start_time})
        return redirect("esp8266-avrisp.herokuapp.com")


listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

def task():
    with app.app_context():
        global TCP_IP
        global TCP_PORT
        global messages
        global page
        start_time = time.time()
        log = AVR.AVR_ISP(TCP_IP,TCP_PORT,page)
        for i in range(0,len(log),2):
            messages.append({'title': log[i], 'content' : log[i+1]})
        messages.append({'title': 'Execution time:', 'content' : time.time() - start_time})



#====