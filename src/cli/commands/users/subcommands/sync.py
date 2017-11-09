import sys
import os

from config import properties
from lib.utils import shell
from lib.users.dao.linux import DAO as LinuxDAO

def create_user_group(user):

    response = {
        "status_code" : 0,
        "out" : None,
        "err" : None
    }

    user_group_exists = False

    shell_response = shell.run(["getent","group",str(user.get_gid())])
    print(shell_response)

    if shell_response["status_code"] != 0:
        response["err"] = "[ERROR] Unable to check user status."
        response["return_code"] = 1
    elif shell_response["out"]:
        user_group_exists = True

    if not user_group_exists:
        print("Creating user group with name <{}> and gid <{}>".format(user.get_username(),str(user.get_gid())))
        shell_response = shell.run(["groupadd","--gid",str(user.get_gid()),user.get_username()])
        print(shell_response)
        if shell_response["status_code"] != 0:
            response["err"] = "[ERROR] Unable to create group."
            response["status_code"] = 1

    return response

def create_user(user):

    response = {
        "status_code" : 0,
        "message" : None
    }

    return response


def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("Checking jerhz users dir <{}>\n".format(properties.jerhz_users_dir))
    if not os.path.isdir(properties.jerhz_users_dir):
        print("[ERROR]: Dir not found or invalid")
        sys.exit(1)

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        response = None

        print("User <{}>".format(user.get_username()))

        print("User group ...")
        response = create_user_group(user)

        print("")

    print("<<< Done.")
