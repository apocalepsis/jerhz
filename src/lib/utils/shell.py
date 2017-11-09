from subprocess import Popen, PIPE, STDOUT

def run(cmd,pshell=False,cwdir=None):

    response = {
        "status_code" : 0,
        "out" : None,
        "err" : None
    }

    p = Popen(cmd,shell=pshell,stdout=PIPE, stdin=PIPE, stderr=STDOUT,cwd=cwdir)
    print("RETURN CODE: " + str(p.returncode)
    out, err = p.communicate()

    if out:
        response["out"] = out.decode("utf-8").strip()
    if err:
        response["status_code"] = 1
        response["err"] = err.decode("utf-8").strip()

    return response
