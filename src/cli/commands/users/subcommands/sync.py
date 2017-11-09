import sys
import os

from config import properties
from lib.utils import shell
from lib.users.dao.linux import DAO as LinuxDAO

def create_user_group(user):

    response = {
        "status_code" : 0,
        "message" : None
    }

    user_group_exists = False

    result = shell.run(["getent","group",user.get_gid()])
    print(result)

    if result["return_code"] != 0:
        print("[ERROR] Unable to check user status.")
        response["status_code"] = 1
    elif result["out"]:
        user_group_exists = True

    if not user_group_exists:
        print("Creating user group with name <{}> and gid <{}>".format(user.get_username(),user.get_gid()))
        result = shell.run(["groupadd","-gid",user.get_gid(),user.get_username()])
        print(result)
        if result["return_code"] != 0:
            print("[ERROR] Unable to check user status.")
            response["status_code"] = 1

    return response

def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("Checking jerhz users dir <{}>".format(properties.jerhz_users_dir))
    if not os.path.isdir(properties.jerhz_users_dir):
        print("[ERROR]: Dir not found or invalid")
        sys.exit(1)

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        response = None

        print("User <{}>".format(user.get_username()))

        response = create_user_group(user)
        print(response)

        print("")

    print("<<< Done.")
