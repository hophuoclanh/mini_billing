import pymysql.cursors
from fastapi import FastAPI, Response, HTTPException
from function.user import User
from function.position import Position
from function.orders import Orders
from function.authentication_function import Authentication_Function
app = FastAPI()
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Hong.Lac@2003',
    db='mini_billing'
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

orders = Orders(connection)

@app.get('/orders/{order_id}')
def get_order(order_id: int):
    order = orders.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.post('/orders')
def create_order(order_data: dict):
    user_id = order_data.get("user_id")
    order_details = order_data.get("order_details")

    if not user_id or not order_details:
        raise HTTPException(status_code=400, detail="Invalid order data")

    order = orders.create_order(order_data)

    return order

@app.put('/orders/{order_id}')
def update_order(order_id: int, order_data: dict):
    user_id = order_data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid order data")

    order = orders.update_order(order_id, user_id)
    return order

@app.delete('/orders/{order_id}')
def delete_order(order_id: int):
    success = orders.delete_order(order_id)

    if not success:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order deleted"}


authentication_function= Authentication_Function(connection)
@app.get('/authentication_function/{authentication_function_id}')
def get_authentication_function(authentication_function_id:str):
    return authentication_function.get(authentication_function_id)

@app.get('/authentication_function')
def get_all_authentication_function():
    return authentication_function.get('*')

@app.post('/authentication_function')
def create_authentication_function(authentication_function_json: dict):
    return authentication_function.post(authentication_function_json)

@app.put('/authentication_function/{authentication_function_id}')
def update_authentication_function(authentication_function_id: str, authentication_function_json: dict):
    return authentication_function.put(authentication_function_id,authentication_function_json)

@app.delete('/authentication_function/{authentication_function_id}')
def delete_authentication_function(authentication_function_id: str):
    return authentication_function.delete(authentication_function_id)