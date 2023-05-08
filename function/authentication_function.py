import pymysql.cursors
from fastapi import FastAPI, Response
import uuid

class Authentication_Function:
    def __init__(self, connection):
        self.connection = connection
    def get(self, authentication_function_id):
        if authentication_function_id != '*':
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `authentication_function` WHERE `authentication_function_id`=%s"
                cursor.execute(sql, (authentication_function_id))
                result = cursor.fetchone()
                if result is not None:
                    res = {
                        'authentication_function_id': result[0],
                        'authentication_function_name': result[1]
                    }
                    return res
                else:
                    return Response(content="Error", status_code=404)

        else:
            with self.connection.cursor() as cursor:
                # Read all records
                sql = "SELECT * FROM `authentication_function`"
                cursor.execute(sql)
                result = cursor.fetchall()
                res = []
                for row in result:
                    temp = {
                        'authentication_function_id': row[0],
                        'authentication_function_name': row[1]

                    }
                    res.append(temp)
                return res

    def post(self, authentication_function):
        with self.connection.cursor() as cursor:
            # Create a new record
            authentication_function_id = uuid.uuid4()
            sql = "INSERT INTO `authentication_function` (`authentication_function_id`,`authentication_function_name`) VALUES (%s,%s)"
            cursor.execute(sql, (
                str(authentication_function_id), authentication_function['authentication_function_name']))
            self.connection.commit()
            return {'authentication_function_id': str(authentication_function_id)}

    def put(self, authentication_function_id, authentication_function):
        with self.connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `authentication_function` SET `authentication_function_name`=%s WHERE `authentication_function_id`=%s"
            cursor.execute(sql, (authentication_function['authentication_function_name'], authentication_function_id))
            self.connection.commit()
            return Response(status_code=204)

    def delete(self, authentication_function_id):
        with self.connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `authentication_function` WHERE `authentication_function_id`=%s"
            cursor.execute(sql, (authentication_function_id))
            self.connection.commit()
            return Response(status_code=204)



