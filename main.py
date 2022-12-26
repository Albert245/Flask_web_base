from flask import Flask, render_template, request, url_for, flash, redirect, session
import os
import DataProcess as DP
import AVRtool as AVR
import time
import threading
import pyrebase
from datetime import timedelta




# ...
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024*32
app.secret_key = '1709'
app.config['ALLOWED_EXTENSIONS'] = {'.hex'}
# app.config['SERVER_NAME'] = 'https://esp8266-avrisp.herokuapp.com'
app.permanent_session_lifetime = timedelta(days = 7)

messages = [{'title': 'Debug Terminal',
             'content': 'Below are debug output'},
            {'title': 'TCP/IP',
             'content': '113.172.96.69 : 328'}
            ]

count = 0

# ...

TCP_IP =  '113.172.96.69'
TCP_PORT = 328

# ...



# ...

# Pyfirebase=========================================================
config = {
    'apiKey': "AIzaSyD6Dh9kEZNAba3o6FWne0rIINNiUB6qc0Y",
    'authDomain': "smart-motorbike-system.firebaseapp.com",
    'databaseURL': "https://smart-motorbike-system-default-rtdb.asia-southeast1.firebasedatabase.app",
    'projectId': "smart-motorbike-system",
    'storageBucket': "smart-motorbike-system.appspot.com",
    'serviceAccount':"serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth
storage = firebase.storage()

# Use for store a file to firebase storage
def uploadfirebase(file_name):
    storage.child(file_name).put(file_name)


# Use for download a file to firebase storage
def downloadfirebase(file_name):
    storage.child(file_name).download(file_name)

# End - Pyfirebase=========================================================


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
        # session['messages'] = messages
        # return redirect(url_for("upload"))

#===========================================[ APP ]===========================================================
@app.route('/')
def index():
    global messages
    session.permanent = True
    if 'messages' in session:
        if len(session['messages']) > len(messages):
            messages = session['messages']
    session['messages'] = messages
    time.sleep(1)
    return render_template('index.html', messages=session['messages'])

@app.route('/hex', methods=('GET', 'POST'))
def hex():
    if 'current_hex' in session:
        if 'last_hex' in session:
            if session['current_hex'] != session['last_hex']:
                return session['current_hex']
            else:
                return 'None'
        return session['current_hex']
    else:
        return 'None'
        
@app.route('/refresh', methods=('GET', 'POST'))
def refresh():
    if 'messages' in session:
        session.pop('messages', None)
    return redirect(url_for('index'))

@app.route('/upload', methods = ('GET','POST'))
def upload():
    session.permanent = True
    if request.method == 'POST':
        global TCP_IP
        global TCP_PORT
        global count
        if 'count' in session:
            count = session['count']
        session['count'] = count
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
        session['count'] = count
        extension = os.path.splitext(file.filename)[1]
        filename = os.path.splitext(file.filename)[0]
        # realpath = os.path.realpath(file.filename)
        Block = []
        if file:
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                return 'Not a hex file'
            for line in file.readlines():
                Block.append(str(line.rstrip()))
            page = DP.convert_hex_file(Block)
            page_txt = DP.convert_raw(Block)
            if 'current_hex' in session:
                session['last_hex'] = session['current_hex']
            session['current_hex'] = page_txt
            new_txt = filename+'.txt'
            with open(new_txt, 'w') as f:
                for row in page_txt:
                    f.write(str(row))
                    print(str(row))
            uploadfirebase(new_txt)
            MyWorker(page)
            messages.append({   'title': 'OTA state no.'+str(count),
                                'content' : 'The program OTA is running in the background, please wait for a minutes'})
            session['messages'] = messages
            return redirect(url_for('index'))
        # except:
        #     return 'Not allowed'
        
    return render_template('upload.html')