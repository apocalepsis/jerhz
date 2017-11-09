import os

from config import properties
from lib.users.dao.linux import DAO as LinuxDAO

def run(args):

    print(">>> Sync in progress, please wait ... \n")

    print("Checking jerhz dir <{}>\n".format(properties.jerhz_efs_dir))
    if not os.path.isdir(properties.jerhz_efs_dir):
        print("[ERROR]: Dir not found or invalid")
        sys.exit(1)

    user_dao_linux = LinuxDAO()

    user_list = user_dao_linux.get_all()

    for user in user_list:

        print("User <{}> status".format(user.get_username()))
        print("")

    print("<<< Done.")
