from database.DB_connect import DBConnect
from model.go_product import GoProduct


class DAO():

    @staticmethod
    def getAllColors():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = "SELECT DISTINCT(Product_color) FROM go_products"
        cursor.execute(query)
        for row in cursor:
            result.append(row["Product_color"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT Product_number, Product_line, Product_type, Product, Product_brand, Product_color, Unit_cost, Unit_price
                    FROM go_products WHERE Product_color=%s"""
        cursor.execute(query, (color, ))
        for row in cursor:
            result.append(GoProduct(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(year, color):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t1.Product_number as prod1, t2.Product_number as prod2, COUNT(distinct t1.`Date`) as peso
                    from (select p.Product_number, s.`Date`, s.Retailer_code
                            from go_daily_sales s, go_products as p
                            where YEAR(s.`Date`) = %s and s.Product_number = p.Product_number and Product_color = %s) as t1,
                         (select p.Product_number, s.`Date`, s.Retailer_code
                            from go_daily_sales s, go_products as p
                            where YEAR(s.`Date`) = %s and s.Product_number = p.Product_number and Product_color = %s) as t2
                    where t1.Product_number > t2.Product_number and t1.`Date` = t2.`Date` and t1.Retailer_code = t2.Retailer_code
                    group by t1.Product_number, t2.Product_number"""
        cursor.execute(query, (year, color, year, color))
        for row in cursor:
            result.append((row["prod1"], row["prod2"], row["peso"]))
        cursor.close()
        conn.close()
        return result