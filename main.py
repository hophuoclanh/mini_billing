import pymysql.cursors
from fastapi import FastAPI, Response
from function.user import User
from function.position import Position
from function.orders import Orders

app = FastAPI()
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Cao.Dien@123',
    db='mini billing'
)

user = User(connection)

@app.get('/users/{user_id}')
def get_user(user_id: str):
    return user.get(user_id)

@app.get('/users')
def get_all_users():
    return user.get('*')

@app.post('/users')
def create_user(user_json: dict):
    return user.post(user_json)

@app.put('/users/{user_id}')
def update_user(user_id: str, user_json: dict):
    return user.put(user_id, user_json)

@app.delete('/users/{user_id}')
def delete_user(user_id: str):
    return user.delete(user_id)

position = Position(connection)

@app.get('/positions/{position_id}')
def get_position(position_id: str):
    return position.get(position_id)

@app.get('/positions')
def get_all_positions():
    return position.get('*')

@app.post('/positions')
def create_position(position_json: dict):
    return position.post(position_json)

@app.put('/positions/{position_id}')
def update_position(position_id: str, position_json: dict):
    return position.put(position_id, position_json)

@app.delete('/positions/{position_id}')
def delete_user(position_id: str):
    return position.delete(position_id)

orders= Orders(connection)
@app.get('/orders/{order_id}')
def get_order(order_id:str):
    return orders.get(order_id)

@app.get('/orders')
def get_all_orders():
    return orders.get('*')

@app.post('/orders')
def create_order(order_json: dict):
    return orders.post(order_json)

@app.put('/orders/{order_id}')
def update_order(order_id: str, order_json: dict):
    return orders.put(order_id,order_json)

@app.delete('/orders/{order_id}')
def delete_order(order_id: str):
    return orders.delete(order_id)