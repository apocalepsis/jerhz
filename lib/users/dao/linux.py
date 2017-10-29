import mysql.connector as mysql

from config import properties
from lib.users.model.linux import User

class DAO:

    db_host = properties.linux_db_host
    db_name = properties.linux_db_name
    db_user = properties.linux_db_user
    db_password = properties.linux_db_password

    def save(self,user):

        found = len(self.get_by_attr("username",user.get_username())) > 0

        if found:
            raise Exception("A user with username <{}> already exists".format(user.get_username()))

        found = len(self.get_by_attr("uid",user.get_uid())) > 0

        if found:
            raise Exception("A user with uid <{}> already exists".format(user.get_uid()))

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "INSERT INTO users VALUES ('{}','{}','{}',{},{})".format(
                user.get_username(),user.get_password(),user.get_type(),user.get_uid(),user.get_gid())

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_by_attr(self,attr,value):

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "DELETE FROM users WHERE {}='{}'".format(attr,value)

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_all(self):

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "DELETE FROM users"

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_by_attr(self,attr,value):

        result = []

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "SELECT * FROM users WHERE {}='{}'".format(attr,value)

            cursor = conn.cursor(buffered=True)
            cursor.execute(sql)

            for row in cursor:
                user = User(row[0],row[1],row[2],row[3],row[4])
                result.append(user)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def get_all(self):

        result = []

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "SELECT * FROM users ORDER BY username"

            cursor = conn.cursor(buffered=True)
            cursor.execute(sql)

            for row in cursor:
                user = User(row[0],row[1],row[2],row[3],row[4])
                result.append(user)

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result
