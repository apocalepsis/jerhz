import sys

from cli.users import commands as users_commands

def display_help():
    print("""
Usage:
    jerhz users [options]

Available Options:
    [parameter]
        Is an immediate action
    [command]
        Can have command(s) and/or parameter(s)

Available Parameters:
    [-h | -help]
        Type: bool
        Required: No

Available Commands:
    [create-user]
        Creates a new user
    [get-all]
        Get all users
    [get-user]
        Get a specific user
    [update-user]
        Update parameter(s) of a specific user
    [delete-all]
        Delete all users
    [delete-user]
        Deletea specific user
    """)

def run(args):

    option = None

    try:
        option = args.pop(0)
    except:
        print("[ERROR] Unable to read option. Please use -h or -help for more information")
        sys.exit(1)

    if option in ["-h","-help"]:
        display_help()

    elif option in ["create-user"]:
        pass
        users_commands.create_user.run(args)

    elif option in ["get-all"]:
        pass

    elif option in ["get-user"]:
        pass

    elif option in ["update-user"]:
        pass

    elif option in ["delete-all"]:
        pass

    elif option in ["delete-user"]:
        pass

    else:
        print("[ERROR] Invalid option <{}>. Please use -h or -help for more information".format(option))
        sys.exit(1)
