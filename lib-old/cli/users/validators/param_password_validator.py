import re

def run(password):
    if not password:
        return False
    else:
        m = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,20}$")
        return m.match(password)
