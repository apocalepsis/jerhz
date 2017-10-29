import sys

# from lib.users.model.linux import User as LinuxUser
from lib.users.dao.linux import DAO as LinuxDAO
from lib.utils import cipher

def run(args):

    try:
        user_dao = LinuxDAO()
        user_list = user_dao.get_all()
        for user in user_list:
            user.set_password(cipher.aes.decrypt(user.get_password()).decode("utf-8"))
            print(user)
    except Exception as e:
        print("[ERROR] {}".format(e))
