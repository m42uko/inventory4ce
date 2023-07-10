message = ""
oldmessage = ""

def set_message(text):
    global message
    global oldmessage
    message = text

def get_message():
    global message
    global oldmessage
    if oldmessage != message:
        oldmessage = message
        return message
    else:
        return ""