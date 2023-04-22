import uuid
import pymysql
from fastapi import Response


class User:
    def __init__(self, connection):
        self.connection = connection

    def get(self, user_id):
        if user_id != '*':
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `user` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id))
                result = cursor.fetchone()
                if result is not None:
                    res = {
                        'user_id': result[0],
                        'user_name': result[1],
                        'email': result[2],
                        'phone': result[3],
                        'address': result[4],
                        'role': result[5]
                    }
                    return res
                else:
                    return Response(content="User not found", status_code=404)

        else:
            with self.connection.cursor() as cursor:
                # Read all records
                sql = "SELECT * FROM `user`"
                cursor.execute(sql)
                result = cursor.fetchall()
                res = []
                for row in result:
                    temp = {
                        'user_id': row[0],
                        'user_name': row[1],
                        'email': row[2],
                        'phone': row[3],
                        'address': row[4],
                        'position_id': row[5]
                    }
                    res.append(temp)
                return res

    import uuid

    def post(self, user):
        with self.connection.cursor() as cursor:
            # Create a new record
            user_id = uuid.uuid4()
            sql = "INSERT INTO `user` (`user_id`, `user_name`, `email`, `phone`, `address`, `role`) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (
            user_id, user['user_name'], user['email'], user['phone'], user['address'], user['role']))
            self.connection.commit()
            return {'user_id': str(user_id)}

    def put(self, user_id, user):
        with self.connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `user` SET `user_name`=%s, `phone`=%s, `email`=%s, `address`=%s, `position_id`=%s WHERE `user_id`=%s"
            cursor.execute(sql, (user['user_name'], user['email'], user['phone'], user['address'], user['position_id'], user_id))
            self.connection.commit()
            return Response(status_code=204)

    def delete(self, user_id):
        with self.connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `user` WHERE `user_id`=%s"
            cursor.execute(sql, (user_id))
            self.connection.commit()
            return Response(status_code=204)
