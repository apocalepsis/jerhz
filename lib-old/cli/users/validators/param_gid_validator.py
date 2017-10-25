def run(gid):
    if not gid:
        return False
    else:
        m = re.compile("^\d{4,8}$")
        return m.match(gid)
