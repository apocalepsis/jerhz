import sys

from lib.users.model.linux import User as LinuxUser
from lib.users.dao.linux import DAO as LinuxDAO
from lib.users.validator.linux import Validator as LinuxValidator
from lib.utils import cipher

params = {
    "username" : None,
    "password" : None,
    "type" : None,
    "uid" : None,
    "gid" : None
}

def display_help():
    print("""
Usage:
    jerhz-cli.py users create-user [options]

Available Options:
    [parameter]
        Is an immediate action

Available Parameters:
    [-h | -help]
        Type: bool
        Required: no
    [-username <value>]
        Type: string
        Required: yes
        Notes:
            * Must be between <8-20> characters length.
            * Only alphanumeric and underscore characters are accepted.
    [-password <value>]
        Type: string
        Required: yes
        Notes:
            * Must be between <8-20> characters length.
            * Must include at least one of the special characters #$@!%&*?
            * Must include at least one upper and lower case letters
            * Must include at least one digit
    [-type <system|standard>]
        Type: choice
        Required: yes
        Notes:
            * Choose system if you want to create a user application management.
            * Choose standard if you want to create a user for application usage.
    [-uid <value>]
        Type: integer
        Required: yes
        Notes:
            * Must be between <4-8> digits length.
    [-gid <value>]
        Type: integer
        Required: yes
        Notes:
            * Must be between <4-8> digits length.
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

        elif p in ["-username"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["username"] = v

        elif p in ["-password"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["password"] = v

        elif p in ["-type"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["type"] = v

        elif p in ["-uid"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["uid"] = v

        elif p in ["-gid"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            params["gid"] = v

        else:
            print("[ERROR] Invalid parameter <{0}>".format(p))
            sys.exit(1)

    validator = LinuxValidator()

    p = params["username"]
    if not validator.is_valid_username(p):
        print("[ERROR] Invalid value <{}> for parameter <username>".format(p))
        sys.exit(1)

    p = params["password"]
    if not validator.is_valid_password(p):
        print("[ERROR] Invalid value <{}> for parameter <password>".format(p))
        sys.exit(1)
    else:
        params["password"] = cipher.aes.encrypt(params["password"]).decode("utf-8")

    p = params["type"]
    if not validator.is_valid_type(p):
        print("[ERROR] Invalid value <{}> for parameter <type>".format(p))
        sys.exit(1)

    p = params["uid"]
    if not validator.is_valid_uid(p):
        print("[ERROR] Invalid value <{}> for parameter <uid>".format(p))
        sys.exit(1)

    p = params["gid"]
    if not validator.is_valid_gid(p):
        print("[ERROR] Invalid value <{}> for parameter <gid>".format(p))
        sys.exit(1)

    try:
        user = LinuxUser(params["username"],params["password"],params["type"],params["uid"],params["gid"])
        user_dao = LinuxDAO()
        user_dao.save(user)
    except Exception as e:
        print("[ERROR] {}".format(e))
