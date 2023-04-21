import pymysql.cursors
from fastapi import FastAPI, Response

app = FastAPI()
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='pLkt0987...@',
    db='minibilling'
)

class Position:
    def get(self, position_id):
        if position_id != '*':
            with connection.cursor() as cursor:
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
                    return Response(content="User not found", status_code=404)

        else:
            with connection.cursor() as cursor:
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
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `position` (`role`) VALUES (%s)"
            cursor.execute(sql, (position['role']))
            connection.commit()
            position_id = cursor.lastrowid
            return {'user_id': position_id}

    def put(self, position_id, position):
        with connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `position` SET `role`=%s WHERE `position_id`=%s"
            cursor.execute(sql, (position['role'], position_id))
            connection.commit()
            return Response(status_code=204)

    def delete(self, position_id):
        with connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `position` WHERE `position_id`=%s"
            cursor.execute(sql, (position_id))
            connection.commit()
            return Response(status_code=204)

position = Position()

@app.get('/positions/{position_id}')
def get_position(position_id: str):
    return position.get(position_id)

@app.get('/positions')
def get_all_positions():
    return position.get('*')

@app.post('/positions')
def create_position(position: dict):
    return position.post(position)

@app.put('/positions/{position_id}')
def update_position(position_id: str, position: dict):
    return position.put(position_id, position)

@app.delete('/positions/{position_id}')
def delete_user(position_id: str):
    return position.delete(position_id)

