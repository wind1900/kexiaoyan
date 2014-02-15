import os.path
import datetime

def need_update(filename):
    try:
        modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
    except:
        return True
    current_time = datetime.datetime.now()
    seconds = (current_time - modify_time).total_seconds()
    if seconds > 3600 or modify_time.hour != current_time.hour:
        return True
    return False
    
def get_filename(name):
    s = name.rfind(".") + 1
    filename = os.path.join(os.path.dirname(__file__), name[s:] + ".tmp")
    return filename
