import pymysql
from datetime import datetime
import time

class Orders:
    def __init__(self, connection):
        self.connection = connection

    def get_order(self, order_id):
        with self.connection.cursor() as cursor:
            sql = "SELECT * FROM orders WHERE order_id = %s"
            cursor.execute(sql, (order_id,))
            order = cursor.fetchone()
            return order

    def create_order(self, order_data):
        user_id = order_data.get("user_id")
        order_details = order_data.get("order_details")

        with self.connection.cursor() as cursor:
            # Insert into orders table
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO orders (order_id, user_id, date) VALUES (%s, %s, %s)"
            order_id = int(time.time_ns())
            cursor.execute(sql, (order_id, user_id, order_date))

            # Insert into order_detail table
            for detail in order_details:
                product_id = detail.get("product_id")
                quantity = detail.get("quantity")

                # Check if order_id already exists in order_detail table
                sql_check = "SELECT * FROM order_detail WHERE order_id = %s"
                cursor.execute(sql_check, (order_id,))
                result = cursor.fetchone()

                if result is None:
                    # Order ID does not exist, proceed with inserting order detail
                    sql_insert = "INSERT INTO order_detail (order_id, product_id, quantity) VALUES (%s, %s, %s)"
                    cursor.execute(sql_insert, (order_id, product_id, quantity))

            self.connection.commit()

        return {"order_id": order_id, "user_id": user_id, "order_details": order_details}

    def update_order(self, order_id, user_id):
        with self.connection.cursor() as cursor:
            sql = "UPDATE orders SET user_id = %s WHERE order_id = %s"
            result = cursor.execute(sql, (user_id, order_id))
            self.connection.commit()
            return result > 0

    def delete_order(self, order_id):
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM orders WHERE order_id = %s"
            result = cursor.execute(sql, (order_id,))
            self.connection.commit()
            return result > 0
