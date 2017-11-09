import sys
import os

from config import properties
from lib.utils import shell
from lib.users.dao.linux import DAO as LinuxDAO

def create_user_group(user):

    print("Creating user group <{}> with gid <{}>".format(user.get_username(),user.get_gid()))


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

        user_dir = "{}/{}".format(properties.jerhz_users_dir,user.get_username())
        user_dir_exists = os.path.isdir(user_dir)

        if not user_dir_exists:
            print("User not found, creating environment")
            create_user_group(user)

        print("")

    print("<<< Done.")
