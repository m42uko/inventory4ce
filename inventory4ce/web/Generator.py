import random
import os
from flask import request
from . import User

# TODO: make mp3 work again
#dir_path = './mp3/'
#res = []
#for path in os.listdir(dir_path):
#    # check if current path is a file
#    if os.path.isfile(os.path.join(dir_path, path)):
#        res.append(path)


# TODO: collision detection
def gen_item_id():
        id = f"i{random.randint(1,99999)}"
        return id
      
def try_submit(submit):
    search_value = None
    try:
            search_value = request.form[submit].strip()
    except:
        pass
    return search_value

