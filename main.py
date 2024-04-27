from flask import request, jsonify, render_template
from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_socketio import SocketIO
import pymongo
from datetime import datetime
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'your_secret_key'

uri = "mongodb+srv://Bamidele1:1631324de@mycluster.vffurcu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
dbs = client['test']
day = dbs['day']
user = dbs['User Data']
emaild = dbs['email']
messages = dbs['cmessages']
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/')
def test():
    return render_template('test.html')
@app.route('/varian', methods=['POST'])
def varian():
    first = request.form.get('first')
    last = request.form.get('last')
    email = request.form.get('email')
    number = request.form.get('number')
    appoint = request.form.get('appoint')
    time = request.form.get('time')
    timestamp = datetime.now()
    send = {
        "first": first,
        "last": last,
        "email": email,
        "number": number,
        "time": time,
        "appoint": appoint,
        "timestamp": timestamp
    }
    messages.insert_one(send)
    socketio.emit('data_update')
    return jsonify("done")
@app.route('/inde')
def inde():
    return render_template('index.html')
@app.route('/index', methods=['POST'])
def index():
    # Fetch the sorted data from the database
    sorted_data = list(messages.find({}, {'_id': 0}).sort('timestamp', pymongo.DESCENDING))


    # Return the sorted data as JSON
    return jsonify(sorted_data)

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8080, debug=True)
