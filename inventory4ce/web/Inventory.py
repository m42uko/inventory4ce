import json
from flask import render_template
from . import User
from . import QRCode
from pathlib import Path

QUEUE_PATH = QRCode.get_queue_path()
JSON_PATH = QRCode.get_json_path()

def page(message,qr):
    
    return render_template("Inventory.html", invdata = get_inventory(), userdata = User.get_userlist(), message = message, print_qr = qr)
     
def get_inventory():
    inventory = {}
     
    try:
        with open(JSON_PATH+'storage.json', 'r') as invfile:
            inventory = json.load(invfile)
    except Exception as e:
        print("Creating storage.json")
        Path(JSON_PATH).mkdir(parents=True, exist_ok=True)
        with open(Path(JSON_PATH) / 'storage.json', 'w+') as invfile:
            json.dump({},invfile)
    return inventory

def add_item(id,name,location):
    inventory = get_inventory()
    inventory.update({id: [name,location,"Yes",""]})    
    with open(JSON_PATH+'storage.json', 'w') as file:
        json.dump(inventory,file)
        
def del_item(id):
    inventory = get_inventory()
    users = User.get_userlist()
    try:
        user = inventory[id][3]
        for idx, i in enumerate(users[user],start=0):
            if i == id:
                del users[user][idx]
    except: 
        pass
    
    del inventory[id]
    with open(JSON_PATH+'storage.json', 'w') as invfile:
        json.dump(inventory,invfile)
    with open(JSON_PATH+'user.json', 'w') as userfile:
        json.dump(users,userfile)
