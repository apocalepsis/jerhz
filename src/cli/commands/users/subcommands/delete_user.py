import sys

from lib.users.dao.linux import DAO as LinuxDAO
from lib.users.dao.zeppelin import DAO as ZeppelinDAO

from lib.users.validator.linux import Validator as LinuxValidator

params = {
    "attr-name" : None,
    "attr-value" : None
}

def display_help():
    print("""
Usage:
    jerhz-cli.py users delete-user [options]

Available Options:
    [parameter]
        Is an immediate action

Available Parameters:
    [-h | -help]
        Type: bool
        Required: no
    [-attr-name <username|type|uid|gid>]
        Type: choice
        Required: yes
    [-attr-value <value>]
        Type: string
        Required: yes
    """)

def run(args):

    if len(args) == 0:
        print("[ERROR] No options found. Please use -h or -help for more information")
        sys.exit(1)

    # MAPPINGS

    while len(args) > 0:

        p = None

        try:
            p = args.pop(0)
        except:
            print("[ERROR] Unable to read parameter. Please use -h or -help for more information")
            sys.exit(1)

        if p in ["-h","-help"]:
            display_help()
            sys.exit(0)

        elif p in ["-attr-name"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["attr-name"] = v

        elif p in ["-attr-value"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["attr-value"] = v

        else:
            print("[ERROR] Invalid parameter <{0}>".format(p))
            sys.exit(1)

    validator = LinuxValidator()

    p = params["attr-name"]
    if not validator.is_valid_attr_name(p):
        print("[ERROR] Invalid value <{}> for parameter <attr-name>".format(p))
        sys.exit(1)

    p = params["attr-value"]
    if not validator.is_valid_attr_value(p):
        print("[ERROR] Invalid value <{}> for parameter <attr-value>".format(p))
        sys.exit(1)

    user_dao_linux = LinuxDAO()
    user_dao_zeppelin = ZeppelinDAO()

    user_list = user_dao_linux.get_by_attr(params["attr-name"],params["attr-value"])

    for user in user_list:
        try:
            user_dao_zeppelin.delete_by_attr("username",user.get_username())
            user_dao_linux.delete_by_attr("username",user.get_username())
        except Exception as e:
            print("[ERROR] {}".format(e))
