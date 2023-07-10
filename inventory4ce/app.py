import json
from flask import Flask, jsonify,render_template, request, session
import logging
import os
from .web import User
from .web import QRCode
from .web import Inventory
from .web import Message
from .web import Generator
from markupsafe import escape
from pathlib import Path

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder="static/", static_url_path="")

app.secret_key = 'Ghadaw7dashd37z8d' #Key for Flasksession 

#ensure the path exists 
QUEUE_PATH = QRCode.get_queue_path()
JSON_PATH = QRCode.get_json_path()

def init_db():
    Path(QUEUE_PATH).mkdir(parents=True, exist_ok=True)

@app.route('/user', methods = ['POST']) #Update current user in session
def select():
    if request.method == 'POST':
        sel_user = request.get_json()
        if sel_user:
            session["registered_user"] = sel_user["user"]
    return ""

@app.route('/play', methods = ['POST'])
def play():
    # Generator.play_sound()
    return ""
@app.route("/")
def QRRoute():
    return QRCode.page()

@app.route("/users", methods=['POST','GET']) #page of user
def tasksRoute():
    message = None
    user = None
    if request.method == 'POST':
        userlist =User.get_userlist()
        if "add_submit" in request.form:
            user = request.form['add'].capitalize()
            if user not in userlist.keys() and user != "":
                User.add_user(user)
                message = f"{user} added"
            else:
                message = f"{user} already exists"
                
                
        if "del_submit" in request.form:
            user = request.form['del'].capitalize()
            if user in userlist.keys():
                User.del_user(user)
                message = f"{user} deleted"
            else:
                message = f"{user} doesn't exist"
    return User.page(message)

@app.route("/inventory", methods=['POST','GET'])
def invRoute():
    message = None
    inventory = None
    if request.method == 'POST':
        send_qr = None                                        
        add_id = Generator.try_submit("addid")
        add_name = Generator.try_submit("name")
        add_location = Generator.try_submit("location")
        print_qrcode = Generator.try_submit("checkbox")
        del_id = Generator.try_submit("del")
        del_inv = Generator.try_submit("delete")
        
        if add_name and add_location:
            with open(JSON_PATH+'storage.json', 'r') as invfile:
                inventory = json.load(invfile)
            notice = ""
            if not add_id or (add_id in inventory.keys()):
                add_id = Generator.gen_item_id()
                notice = f" and generated Id: {add_id}"
                
            if print_qrcode:
               send_qr = add_id
            Inventory.add_item(add_id,add_name,add_location)
            if not print_qrcode:
                with open(QUEUE_PATH+'Queue.txt','a') as queue:
                    queue.write(f"{add_id}\n")  
            message = f"{add_name} added" + notice
        elif add_name or add_location:
            message = "Couldn't add item: data missing"   
        if del_id:
            Inventory.del_item(del_id)
            message=f"{del_id} deleted"
        if del_inv:
            Inventory.del_item(del_inv)
        return Inventory.page(message,send_qr)   
    return Inventory.page(message,None)


@app.route('/functions', methods = ['POST'])
def call_python():
    if request.method == 'POST':
        jsdata = request.get_json()

        if jsdata['method'] == 'ret':
            User.ret(session["registered_user"],jsdata['barcode'])
            
        if jsdata['method'] == 'borrowfrom':
            User.ret(jsdata['person'],jsdata['barcode'])
            User.borrow(session["registered_user"],jsdata['barcode'])
        if jsdata['method'] == 'borrow':
            User.borrow(session["registered_user"],jsdata['barcode'])    
    return ""

@app.route('/options', methods = ['POST','GET'])
def options():
    if request.method == 'POST':
        person = session["registered_user"]
        jsdata = request.get_json()
        id = jsdata['id']  
        info = User.has_item(person,id)
        if info == "Error": 
            return ""
        if jsdata['borrow'] == 'True':
            if info == "no":
                User.borrow(person,id)
                Message.set_message(f"{id} borrowed")
            elif info == "yes":
                Message.set_message("You already borrowed this item")
            else:
                Message.set_message("Already borrowed from another person")    
        if jsdata['ret'] == 'True':
            if info == "otherperson":
                Message.set_message(f"{id} borrowed frome someone else")
            if info == "yes":
                User.ret(person,id)
                Message.set_message(f"{id} returned")
        if jsdata['del'] == 'True':
            Inventory.del_item(id)
            Message.set_message(f"{id} deleted")  
        return ""

@app.route('/options/response', methods = ['POST','GET'])
def response():
    message = Message.get_message()
    return jsonify(message)


# das ist unten ist einfach kompletter Quatsch
# muss in eine extra file abstrahiert werden, ein json objekt sein und
# eventuell garnicht serialisiert werden
@app.route('/queue', methods = ['POST','GET'])
def queue():
    try:
        with open(QUEUE_PATH+'Queue.txt','r') as queue:
            queue = f.read().splitlines()
    except Exception as e:
        print("Creating Queue.txt")
        Path(QUEUE_PATH).mkdir(parents=True, exist_ok=True)
        with open(Path(QUEUE_PATH) / 'Queue.txt', 'w+') as queuefile:
            queuefile.write("")
        queue = []
    with open(QUEUE_PATH+"Queue.txt",'r') as file:
        text = file.read()
        with open(QUEUE_PATH+"OldQueue.txt",'a+') as oldfile:
            oldfile.write(text+"\n")
        with open(QUEUE_PATH+"Queue.txt",'w') as clearfile:
            clearfile.write("")
    return jsonify(queue)

@app.route('/getdata', methods = ['POST','GET'])
def send_data():
    return jsonify(userdata = User.get_userlist())

@app.route('/getuser', methods = ['POST','GET'])
def send_user():
    return session["registered_user"]


def run():
    app.run(debug=os.environ.get('INVENTORY_DEBUG','').lower() in ['on','true','yes'],
            host=os.environ.get('INVENTORY_HOST','127.0.0.1'),
            port=int(os.environ.get('INVENTORY_PORT',3000)),
            ssl_context='adhoc'
            )

if __name__ == '__main__':
    
    run()
    

