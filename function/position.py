import pymysql.cursors
from fastapi import FastAPI, Response
import uuid

class Position:
    def __init__(self, connection):
        self.connection = connection
    def get(self, position_id):
        if position_id != '*':
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `position` WHERE `position_id`=%s"
                cursor.execute(sql, (position_id))
                result = cursor.fetchone()
                if result is not None:
                    res = {
                        'position_id': result[0],
                        'role': result[1]
                    }
                    return res
                else:
                    return Response(content="Error", status_code=404)

        else:
            with self.connection.cursor() as cursor:
                # Read all records
                sql = "SELECT * FROM `position`"
                cursor.execute(sql)
                result = cursor.fetchall()
                res = []
                for row in result:
                    temp = {
                        'position_id': row[0],
                        'role': row[1]

                    }
                    res.append(temp)
                return res

    def post(self, position):
        with self.connection.cursor() as cursor:
            # Create a new record
            position_id = uuid.uuid4()
            sql = "INSERT INTO `position` (`position_id`,`role`) VALUES (%s,%s)"
            cursor.execute(sql, (
                str(position_id), position['role']))
            self.connection.commit()
            return {'position_id': str(position_id)}

    def put(self, position_id, position):
        with self.connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `position` SET `role`=%s WHERE `position_id`=%s"
            cursor.execute(sql, (position['role'], position_id))
            self.connection.commit()
            return Response(status_code=204)

    def delete(self, position_id):
        with self.connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `position` WHERE `position_id`=%s"
            cursor.execute(sql, (position_id))
            self.connection.commit()
            return Response(status_code=204)



