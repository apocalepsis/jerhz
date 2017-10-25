import re

def run(username):
    if not username:
        return False
    else:
        m = re.compile("^[0-9a-zA-Z]{8,20}$")
        return m.match(username)
