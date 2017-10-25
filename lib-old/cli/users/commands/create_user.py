import sys
import re
import mysql.connector

from cli.users import validators as users_validators
from cli.daos import users as users_dao

params = {
    "username" : None,
    "password" : None,
    "type" : None,
    "uid" : None,
    "gid" : None,
    "db" : None
}

def display_help():
    print("""
Usage:
    jerhz users create-user [options]

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
            * Must include special characters, letters, numbers.
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
    [-db <value>]
        Type: string
        Required: yes
        Notes:
            * Database must exists, if not it will throw an error

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
            if not v:
                print("[ERROR] Parameter <{0}> is required".format(p))
                sys.exit(1)
            params["username"] = v

        elif p in ["-password"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            if not v:
                print("[ERROR] Parameter <{0}> is required".format(p))
                sys.exit(1)
            params["password"] = v

        elif p in ["-type"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            if not v:
                print("[ERROR] Parameter <{0}> is required".format(p))
                sys.exit(1)
            params["type"] = v

        elif p in ["-uid"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            if not v:
                print("[ERROR] Parameter <{0}> is required".format(p))
                sys.exit(1)
            params["uid"] = v

        elif p in ["-gid"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            if not v:
                print("[ERROR] Parameter <{0}> is required".format(p))
                sys.exit(1)
            params["gid"] = v

        elif p in ["-db"]:
            v = None
            try:
                v = args.pop(0)
            except:
                print("[ERROR] Unable to read value for parameter <{0}>".format(p))
                sys.exit(1)
            if not v:
                print("[ERROR] Parameter <{0}> is required".format(p))
                sys.exit(1)
            params["db"] = v

        else:
            print("[ERROR] Invalid parameter <{0}>".format(p))
            sys.exit(1)

    # VALIDATIONS

    # username
    if not params["username"]:
        print("[ERROR] Parameter <username> is required")
        sys.exit(1)
    if not users_validators.param_username_validator.run(params["username"]):
        print("[ERROR] Invalid value <{0}> for parameter <username>".format(params["username"]))
        sys.exit(1)

    # db
    if not params["db"]:
        print("[ERROR] Parameter <db> is required")
        sys.exit(1)
