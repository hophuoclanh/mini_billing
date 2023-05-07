from fastapi import Response
import datetime
class Orders:
    def __init__(self, connection):
        self.connection = connection

    def get(self, order_id):
        if order_id != '*':
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `orders` WHERE `order_id`=%s"
                cursor.execute(sql, (order_id))
                result = cursor.fetchone()
                if result is not None:
                    res = {
                        'order_id': result[0],
                        'user_id': result[1],
                        'date': result[2],
                        'total_amount': result[3],
                    }
                    return res
                else:
                    return Response(content="order not found", status_code=404)

        else:
            with self.connection.cursor() as cursor:
                # Read all records
                sql = "SELECT * FROM `orders`"
                cursor.execute(sql)
                result = cursor.fetchall()
                res = []
                for row in result:
                    temp = {
                        'order_id': row[0],
                        'user_id': row[1],
                        'date': row[2],
                        'total_amount': row[3],
                    }
                    res.append(temp)
                return res

    def post(self, orders):
        with self.connection.cursor() as cursor:
            # Create a new record
            daynow = datetime.now()
            year = str(daynow.year)[-2:]
            month = str(daynow.month).zfill(2)
            day = str(daynow.day).zfill(2)
            hour = str(daynow.hour).zfill(2)
            minute = str(daynow.minute).zfill(2)
            second = str(daynow.second).zfill(2)
            order_id = year + month + day + hour + minute + second
            X= datetime.daytime.now()
            date= X.isofomat(" ","seconds")
            sql = "INSERT INTO `orders` (`order_id`, `user_id`, `date`, `total_amount`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (
            order_id,date,orders['user_id'],orders['total_amount']))
            self.connection.commit()
            return {'order_id': str(order_id)}

    def put(self, order_id, orders):
        with self.connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `orders` SET `user_id`=%s, `date`=%s, `total_amount`=%s WHERE `order_id`=%s"
            cursor.execute(sql, (orders['user_id'], orders['date'], orders['total_amount'], order_id))
            self.connection.commit()
            return Response(status_code=204)

    def delete(self, order_id):
        with self.connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `orders` WHERE `order_id`=%s"
            cursor.execute(sql, (order_id))
            self.connection.commit()
            return Response(status_code=204)
