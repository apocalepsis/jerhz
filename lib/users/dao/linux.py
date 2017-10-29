import mysql.connector as mysql

from config import properties
from lib.users.model.linux import User

class DAO:

    db_host = properties.linux_db_host
    db_name = properties.linux_db_name
    db_user = properties.linux_db_user
    db_password = properties.linux_db_password

    def save(self,user):

        result = {
            "status" : 0,
            "payload" : None
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "INSERT INTO users VALUES ('{}','{}','{}',{},{})".format(
                user.username,user.password,user.type,user.uid,user.gid)

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            result["status"] = 1
            result["payload"] = e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def delete_by_attr(self,attr,value):

        result = {
            "status" : 0,
            "payload" : None
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "DELETE FROM users WHERE {}='{}'".format(attr,value)

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            result["status"] = 1
            result["payload"] = e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def delete_all(self):

        result = {
            "status" : 0,
            "payload" : None
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "DELETE * FROM users"

            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            result["status"] = 1
            result["payload"] = e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def get_by_attr(self,attr,value):

        result = {
            "status" : 0,
            "payload" : []
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "SELECT * FROM users WHERE {}='{}'".format(attr,value)

            cursor = conn.cursor(buffered=True)
            cursor.execute(sql)

            for row in cursor:
                user = User(username=row[0],password=row[1],type=row[2],uid=row[3],gid=row[4])
                result["payload"].append(user)

        except Exception as e:
            result["status"] = 1
            result["payload"] = e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result

    def get_all(self):

        result = {
            "status" : 0,
            "payload" : []
        }

        conn = None
        cursor = None

        try:

            conn = mysql.connect(host=self.db_host,database=self.db_name,
                user=self.db_user,password=self.db_password)

            sql = "SELECT * FROM users ORDER BY username"

            cursor = conn.cursor(buffered=True)
            cursor.execute(sql)

            for row in cursor:
                user = User(username=row[0],password=row[1],type=row[2],uid=row[3],gid=row[4])
                result["payload"].append(user)

        except Exception as e:
            result["status"] = 1
            result["payload"] = e

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return result
