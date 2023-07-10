import json
from flask import render_template
from . import Inventory
from . import QRCode
from pathlib import Path

QUEUE_PATH = QRCode.get_queue_path()
JSON_PATH = QRCode.get_json_path()

def page(message):
    return render_template("User.html",invdata = Inventory.get_inventory(), userdata = get_userlist(), message = message)

def get_userlist():
    user = {}
    try:
        with open(JSON_PATH+'user.json', 'r') as userfile:
            user = json.load(userfile)
    except Exception as e:
        Path(JSON_PATH).mkdir(parents=True, exist_ok=True)
        with open(Path(JSON_PATH) / 'user.json', 'w+') as userfile:
            json.dump({},userfile)

    return user

def add_user(name):
    # the name is capitalized to avoid name clash with items (starting with i)
    name = name.capitalize()
    users = get_userlist()
    users.update({name: []})    
    with open(JSON_PATH+'user.json', 'w') as file:
        json.dump(users,file)

def del_user(name):
    users = get_userlist()
    del users[name]
    with open(JSON_PATH+'user.json', 'w') as file:
        json.dump(users,file)
        
def borrow(name,code):
    items = Inventory.get_inventory()
    users = get_userlist()
    items[code][2]="No"
    items[code][3]= name
    users[name].append(code)
    with open(JSON_PATH+'user.json', 'w') as file:
        json.dump(users,file)
    with open(JSON_PATH+'storage.json', 'w') as file:
        json.dump(items,file)
        
def ret(name,code):
    users = get_userlist()
    items = Inventory.get_inventory()
    items[code][2]="Yes"
    items[code][3]= ""
    for idx, i in enumerate(users[name],start=0):
            if i == code:
                del users[name][idx]
                print("item in userfile deleted")
    with open(JSON_PATH+'user.json', 'w') as file:
        json.dump(users,file)
    with open(JSON_PATH+'storage.json', 'w') as file:
        json.dump(items,file)
        
def has_item(name,id):
    users = get_userlist()
    try:
        allvalues = users.values()
        print(allvalues)
    except:
        return "Error"
        
    if id in users[name]:
        return "yes"
    
    if id in allvalues:
        return "otherperson"
    
    return "no"
