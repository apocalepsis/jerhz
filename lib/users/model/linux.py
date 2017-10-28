from lib.utils.cipher import AESCipher

class User:

    def __init__(self,username,password,type,uid,gid):
        self.username = username
        self.password = password
        self.type = type
        self.uid = uid
        self.gid = gid

    def __str__(self):
        return "{}|{}|{}|{}|{}".format(self.username,self.password,self.type,self.uid,self.gid)
