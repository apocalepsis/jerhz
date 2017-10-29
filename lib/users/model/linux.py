import re

class User:

    def __init__(self,username,password,type,uid,gid):
        self.set_username(username)
        self.set_password(password)
        self.set_type(type)
        self.set_uid(uid)
        self.set_gid(gid)

    def get_username(self):
        return self.__username

    def set_username(self,username):
        if self.__is_valid_username(username):
            self.__username = username
        else:
            raise ValueError("Illegal value <{}> for argument <username>".format(username))

    def get_password(self):
            return self.__password

    def set_password(self,password):
        if self.__is_valid_password(password):
            self.__password = password
        else:
            raise ValueError("Illegal value <{}> for argument <password>".format(password))

    def get_type(self):
            return self.__type

    def set_type(self,type):
        if self.__is_valid_type(type):
            self.__type = type
        else:
            raise ValueError("Illegal value <{}> for argument <type>".format(type))

    def get_uid(self):
            return self.__uid

    def set_uid(self,uid):
        if self.__is_valid_uid(uid):
            self.__uid = uid
        else:
            raise ValueError("Illegal value <{}> for argument <uid>".format(uid))

    def get_gid(self):
            return self.__gid

    def set_gid(self,gid):
        if self.__is_valid_gid(gid):
            self.__gid = gid
        else:
            raise ValueError("Illegal value <{}> for argument <gid>".format(gid))

    def __is_valid_username(self,username):
        m = re.compile("^[0-9a-zA-Z]{8,20}$")
        return m.match(username)

    def __is_valid_password(self,password):
        m = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#$@!%&*?])[A-Za-z\d#$@!%&*?]{8,20}$")
        return m.match(password)

    def __is_valid_type(self,type):
        m = re.compile("^system|standard$")
        return m.match(type)

    def __is_valid_uid(self,uid):
        m = re.compile("^\d{4,8}$")
        return m.match(uid)

    def __is_valid_gid(self,gid):
        m = re.compile("^\d{4,8}$")
        return m.match(gid)

    def __str__(self):
        return "{}|{}|{}|{}|{}".format(self.__username,self.__password,self.__type,self.__uid,self.__gid)
