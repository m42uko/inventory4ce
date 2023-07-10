from flask import render_template
from . import User
from . import Inventory
import qrcode


QUEUE_PATH = "./_data/qrcodes/"
JSON_PATH = "./_data/db/"

def get_queue_path():    
    return QUEUE_PATH

def get_json_path():    
    return JSON_PATH

def page():
    return render_template("Main.html",userdata = User.get_userlist(), invdata = Inventory.get_inventory())

        
