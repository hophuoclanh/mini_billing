import pymysql.cursors
from fastapi import FastAPI, Response

app = FastAPI()
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='pLkt0987...@',
    db='minibilling'
)

class User:
    def get(self, user_id):
        if user_id != '*':
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `user` WHERE `user_id`=%s"
                cursor.execute(sql, (user_id))
                result = cursor.fetchone()
                if result is not None:
                    res = {
                        'user_id': result[0],
                        'user_name': result[1],
                        'phone': result[2],
                        'email': result[3],
                        'address': result[4],
                        'position_id': result[5]
                    }
                    return res
                else:
                    return Response(content="User not found", status_code=404)

        else:
            with connection.cursor() as cursor:
                # Read all records
                sql = "SELECT * FROM `user`"
                cursor.execute(sql)
                result = cursor.fetchall()
                res = []
                for row in result:
                    temp = {
                        'user_id': row[0],
                        'user_name': row[1],
                        'phone': row[2],
                        'email': row[3],
                        'address': row[4],
                        'position_id': row[5]
                    }
                    res.append(temp)
                return res

    def post(self, user):
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `user` (`user_name`, `phone`, `email`, `address`, `position_id`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user['user_name'], user['phone'], user['email'], user['address'], user['position_id']))
            connection.commit()
            user_id = cursor.lastrowid
            return {'user_id': user_id}

    def put(self, user_id, user):
        with connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `user` SET `user_name`=%s, `phone`=%s, `email`=%s, `address`=%s, `position_id`=%s WHERE `user_id`=%s"
            cursor.execute(sql, (user['user_name'], user['phone'], user['email'], user['address'], user['position_id'], user_id))
            connection.commit()
            return Response(status_code=204)

    def delete(self, user_id):
        with connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `user` WHERE `user_id`=%s"
            cursor.execute(sql, (user_id))
            connection.commit()
            return Response(status_code=204)

user = User()

@app.get('/users/{user_id}')
def get_user(user_id: str):
    return user.get(user_id)

@app.get('/users')
def get_all_users():
    return user.get('*')

@app.post('/users')
def create_user(user: dict):
    return user.post(user)

@app.put('/users/{user_id}')
def update_user(user_id: str, user: dict):
    return user.put(user_id, user)

@app.delete('/users/{user_id}')
def delete_user(user_id: str):
    return user.delete(user_id)

