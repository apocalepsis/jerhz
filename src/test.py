import subprocess

cmd = ["ls","-la"]
cmd = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
o,e = cmd.communicate()
print(o.decode("utf-8"))
print(e.decode("utf-8"))
print(cmd.returncode)
