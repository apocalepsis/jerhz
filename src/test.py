from subprocess import Popen, PIPE, STDOUT

def run(cmd,pshell=False,cwdir=None):

    result = {
        "return_code" : 0,
        "out" : None,
        "err" : None
    }
    p = Popen(cmd,shell=pshell,stdout=PIPE, stdin=PIPE, stderr=STDOUT,cwd=cwdir)
    out, err = p.communicate()
    if out:
        result["out"] = out.decode("utf-8").strip()
    if err:
        result["err"] = err.decode("utf-8").strip()
    return result


group_exists = False

result = run(["getent","group","1000"])
print(result)
if result["return_code"] != 0:
    print("[ERROR] Unable to check user status.")
elif result["out"]:
    group_exists = True
    print("Group exists.")
