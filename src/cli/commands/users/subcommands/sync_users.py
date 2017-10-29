import sys
import os

from subprocess import Popen, PIPE, STDOUT
from config import properties
from lib.utils import shell
from lib.utils import cipher
from lib.users.dao.linux import DAO as LinuxDAO

def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("Checking jerhz dir <{}>\n".format(properties.jerhz_efs_dir))
    if not os.path.isdir(properties.jerhz_efs_dir):
        print("[ERROR]: Dir not found or Invalid")
        sys.exit(1)

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        print("Checking user <{}> status".format(user.get_username()))

        user_exists = False

        result = shell.run(["getent","passwd",user.get_username()])
        print(result)
        if result["return_code"] != 0:
            print("[ERROR] Unable to check user status.")
            continue
        elif result["out"]:
            user_exists = True
            print("User exists.")

        if not user_exists:
            print("Creating user <{}>".format(user.get_username()))
            result = shell.run(["useradd",user.get_username()])
            print(result)
            if result["return_code"] != 0:
                print("[ERROR] Unable to create user.")
                continue
            elif result["out"]:
                continue

        if not user_exists:
            user_password = cipher.aes.decrypt(user.get_password()).decode("utf-8")
            if user_password:
                print("Creating password for user <{}>".format(user.get_username()))
                cmd = "echo '{}' | passwd {} --stdin".format(user_password,user.get_username())
                result = shell.run(cmd,pshell=True)
                print(result)
                user_password = None
                if result["return_code"] != 0:
                    print("[ERROR] Unable to create user password.")
                    continue

        if not user_exists:
            print("Assigning uid <{}> to user <{}>".format(user.get_uid(),user.get_username()))
            result = shell.run(["usermod","-u",str(user.get_uid()),user.get_username()])
            print(result)
            if result["return_code"] != 0:
                print("[ERROR] Unable to assign uid.")
                continue
            elif result["out"]:
                continue

        if not user_exists:

            group_exists = False

            result = shell.run(["getent","group",str(user.get_gid())])
            print(result)
            if result["return_code"] != 0:
                print("[ERROR] Unable to check group status.")
                continue
            elif result["out"]:
                group_exists = True

            print("Assigning gid <{}> to user <{}>".format(user.get_gid(),user.get_username()))
            if not group_exists:
                print("Group not exists, creating it.")
                result = shell.run(["groupadd",str(user.get_username()),"-g",str(user.get_gid())])
                print(result)
                if result["return_code"] != 0:
                    print("[ERROR] Unable to create ggroup.")
                    continue
                elif result["out"]:
                    continue

            if group_exists:
                print("Group exists, adding user.")
                result = shell.run(["usermod","-g",str(user.get_gid()),user.get_username()])
                print(result)
                if result["return_code"] != 0:
                    print("[ERROR] Unable to assign gid to user.")
                    continue
                elif result["out"]:
                    continue

        print("")

    print("<<< Done.")
