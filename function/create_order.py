from fastapi import Response
class Create_Order:
    def __init__(self, connection):
        self.connection = connection

    def get(self, create_order_id):
        if create_order_id != '*':
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `create_order` WHERE `order_id`=%s"
                cursor.execute(sql, (create_order_id))
                result = cursor.fetchone()
                if result is not None:
                    res = {
                        'order_id': result[0],
                        'product_id': result[1],
                        'quantity': result[2],
                        'price_per_unit':result[3],
                        'total_amount_per_unit': result[4]
                    }
                    return res
                else:
                    return Response(content="create order not found", status_code=404)

        else:
            with self.connection.cursor() as cursor:
                # Read all records
                sql = "SELECT * FROM `create_order`"
                cursor.execute(sql)
                result = cursor.fetchall()
                res = []
                for row in result:
                    temp = {
                        'order_id': row[0],
                        'product_id': row[1],
                        'quantity': row[2],
                        'price_per_unit': row[3],
                        'total_amount_per_unit': row[4],
                    }
                    res.append(temp)
                return res

    def post(self, create_order):
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `create_order` (`order_id`, `product_id`, `quantity`,'price_per_unit' ,`total_amount_per_unit`) VALUES (%s, %s, %s,%s, %s)"
            cursor.execute(sql, (
            create_order['order_id'], create_order['product_id'],create_order['quantity'],create_order['price_per_unit'],create_order['total_amount_price_unit']))
            self.connection.commit()
            return {'create success'}

    def put(self, order_id, create_order):
        with self.connection.cursor() as cursor:
            # Update an existing record
            sql = "UPDATE `create_order` SET `product_id`=%s, `quantity`=%s, 'price_per_unit'=%s,'total_amount_per_unit'=%s WHERE `order_id`=%s"
            cursor.execute(sql, (create_order['user_id'], create_order['date'], create_order['total_amount'], order_id))
            self.connection.commit()
            return Response(status_code=204)

    def delete(self, order_id):
        with self.connection.cursor() as cursor:
            # Delete a record
            sql = "DELETE FROM `create_order` WHERE `order_id`=%s"
            cursor.execute(sql, (order_id))
            self.connection.commit()
            return Response(status_code=204)
