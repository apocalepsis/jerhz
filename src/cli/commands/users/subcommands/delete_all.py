import sys

from lib.users.dao.linux import DAO as LinuxDAO

def run(args):

    try:
        user_dao = LinuxDAO()
        user_dao.delete_all()
    except Exception as e:
        print("[ERROR] {}".format(e))
