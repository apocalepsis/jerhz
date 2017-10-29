import sys

from lib.users.dao.linux import DAO as LinuxDAO
from lib.users.dao.zeppelin import DAO as ZeppelinDAO

def run(args):

    try:
        user_dao = LinuxDAO()
        user_dao.delete_all()
        user_dao = ZeppelinDAO()
        user_dao.delete_all()
    except Exception as e:
        print("[ERROR] {}".format(e))
