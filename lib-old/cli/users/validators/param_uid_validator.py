def run(uid):
    if not uid:
        return False
    else:
        m = re.compile("^\d{4,8}$")
        return m.match(uid)