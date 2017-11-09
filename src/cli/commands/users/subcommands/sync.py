import sys
import os

from config import properties
from lib.users.dao.linux import DAO as LinuxDAO

def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("Checking jerhz users dir <{}>".format(properties.jerhz_users_dir))
    if not os.path.isdir(properties.jerhz_users_dir):
        print("[ERROR]: Dir not found or invalid")
        sys.exit(1)

    print("")

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        print("User <{}> status".format(user.get_username()))

        user_dir = "{}/{}".format(properties.jerhz_users_dir,user.get_username()))
        print("Checking user dir <{}>".format(user_dir))
        if not os.path.isdir(user_dir):
            print("[ERROR]: Dir not found or invalid")
            continue

        print("")

    print("<<< Done.")
