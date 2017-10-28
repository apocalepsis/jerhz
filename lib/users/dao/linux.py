import mysql.connector as mysql

from lib.users.model.linux import User as LinuxUser

class DAO:

    db_host="jerhz-cluster.cluster-csdbzz5e1rot.us-east-1.rds.amazonaws.com"
    db_name="linux"
    db_user="dbadmin"
    db_password="Passw0rd!"

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

            cursor = conn.cursor(buffered=True)
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

    def find_by_attr(self,attr,value):

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
                user = LinuxUser(username=row[0],password=row[1],type=row[2],uid=row[3],gid=row[4])
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

    def all(self):

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
                user = LinuxUser(username=row[0],password=row[1],type=row[2],uid=row[3],gid=row[4])
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
