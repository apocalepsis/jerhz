import sys
import os
import re

from subprocess import Popen, PIPE, STDOUT
from config import properties
from lib.utils import shell
from lib.utils import cipher
from lib.users.dao.linux import DAO as LinuxDAO

def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("    Checking jerhz dir <{}>".format(properties.jerhz_efs_dir))
    if not os.path.isdir(properties.jerhz_efs_dir):
        print("        [ERROR]: Dir not found or Invalid")
        sys.exit(1)

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        print("    Validating environment for user <{}>\n".format(user.get_username()))

        result = shell.run(["id","-u",user.get_username()])
        if result["return_code"] != 0:
            print("        [ERROR] Unable to validate environment.")
            sys.exit(1)

        m = re.compile("^\d*$")
        if m.match(result["out"]):
            print("        User <{}> already deployed".format(user.get_username()))
            continue

        print("    Creating user <{}>".format(user.get_username()))
        result = shell.run(["useradd",user.get_username()])
        if result["return_code"] != 0:
            print("        [ERROR] Unable to create user.")
            continue

        user_password = user.get_password()
        if user_password:
            print("    Creating password for user <{}>".format(user.get_username()))
            user_password = cipher.aes.decrypt(user_password).decode("utf-8")
            result = shell.run(["passwd",user_password])
            user_password = None
            if result["return_code"] != 0:
                print("        [ERROR] Unable to create user password.")
                continue

        print("    Assigning uid <{}> to user <{}>".format(user.get_uid(),user.get_username()))
        result = shell.run(["usermod","-u",str(user.get_uid()),user.get_username()])
        if result["return_code"] != 0:
            print("        [ERROR] Unable to assign uid.")
            continue

        print("    Assigning gid <{}> to user <{}>".format(user.get_gid(),user.get_username()))
        result = shell.run(["groupmod","-g",str(user.get_gid()),user.get_username()])
        if result["return_code"] != 0:
            print("        [ERROR] Unable to assign gid.")
            continue

        print("")

    print("<<< Done.")
