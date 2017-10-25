import mysql.connector as mysql

class BaseDAO:

    def __init__(self):
        self.db_host = "jerhz-cluster.cluster-csdbzz5e1rot.us-east-1.rds.amazonaws.com"
        self.db_name = "db"
        self.db_user = "dbadmin"
        self.db_password = "Passw0rd!"

    def test(self):
        try:
            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)
        conn.close()

dao = BaseDAO()
dao.test()
