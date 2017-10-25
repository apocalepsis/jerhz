import re

def run(type):
    if not type:
        return False
    else:
        m = re.compile("^system|standard$")
        return m.match(type)
