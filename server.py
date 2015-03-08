import os
import uuid
import psycopg2
import psycopg2.extras
from flask import Flask, session, render_template
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
#app.secret_key = 'secret'
#app.secret_key = os.urandom(24).encode('hex')

messages = [{'text':'test', 'name':'testName'}]
users = {}
#messages = []
socketio = SocketIO(app)

def connectToDB():
  
  connectionString = 'dbname=ircdb user=postgres password=postgres host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")

def updateRoster():
    names = []
    for user_id in  users:
        print users[user_id]['username']
        if len(users[user_id]['username'])==0:
            names.append('Anonymous')
        else:
            names.append(users[user_id]['username'])
    print 'broadcasting names'
    emit('roster', names, broadcast=True)
    
@socketio.on('connect', namespace='/chat')
def test_connect():
    session['uuid']=uuid.uuid1()
    session['username']='starter name'
    print 'connected'
    
    users[session['uuid']]={'username':'New User'}
    updateRoster()

#connect to db and get any messages already there and print to screen
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    fetch_messages = "select text, username from messages join users on users.id = messages.username"
    cur.execute(fetch_messages)
    messages = cur.fetchall()
    keys = ['text', 'username']

    for message in messages: # print out messages
         message = dict(id(keys, message)) # this should match them up
         print(message)
         emit('message', message)

@socketio.on('message', namespace='/chat')
def new_message(message):
    #tmp = {'text':message, 'name':'testName'}
    
    
    tmp = {'text':message, 'name':users[session['uuid']]['username']} # add timestamp
    messages.append(tmp)
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    message_insert = "INSERT INTO messages VALUES (default, %s, %s)"; # add timestamp
    cur.execute(message_insert, (message, session['id']))
    conn.commit()
    emit('message', tmp, broadcast=True)
    
@socketio.on('identify', namespace='/chat')
def on_identify(message):
    print 'identify' + message
    users[session['uuid']]={'username':message}
    updateRoster()


@socketio.on('login', namespace='/chat')
def on_login(data):
    #print 'login '  + pw
    print 'login' + users['password']
   
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    log_in = "SELECT * FROM users WHERE username = %s AND password = crypt(%s, password)"
    cur.execute(log_in, (data['username'], data['password']))
    result = cur.fetchone()
    #stick login stuff here
    if result:
        users[session['uuid']]={'username': data['username']}
        session['username']=data['username']
        session['id']=result['id']
        print 'You Are Logged In'
        updateRoster()

# need to do search box stuff

    
@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print 'disconnect'
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()

@app.route('/')
def hello_world():
    print 'in hello world'
    return app.send_static_file('index.html')
    #return 'Hello World!'
    #return render_template('index.html')

@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))
    
@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))
    
@app.route('/img/<path:path>')
def static_proxy_img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))
    
if __name__ == '__main__':
    print "A"

    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
     