import pyodbc


class DatabaseConnector:
    def __init__(self):
        self.db_url = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=W3145\\MSQL19;DATABASE=LUZ24;UID=u24;PWD="

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.db_url)
            self.cursor = self.conn.cursor()
            print("Connection established")
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")

    def fetch_invoices_with_calosc_tak(self):
        query = "SELECT * FROM dbo.LUZ_Zwroty WHERE czy_calosc = 'tak' AND czy_zwrocone = '0'"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error fetching symbols: {e}")
            return []

    def fetch_invoices(self):
        query = "SELECT * FROM dbo.LUZ_Zwroty WHERE czy_zwrocone = '0'"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except pyodbc.Error as e:
            print(f"Error fetching symbols: {e}")
            return []

    def fetch_lp_for_invoice(self, numeriai, sku):
        query = """
        SELECT DISTINCT [LP]
        FROM [LUZ24].[dbo].[faktury_lp]
        WHERE numer_iai = ? AND SKU = ?
        """
        try:
            # Ensure numeriai and sku are treated as strings
            numeriai_str = f"{numeriai}"
            sku_str = f"{sku}"
            print(f"Executing query: {query} with numeriai: {numeriai_str} and sku: {sku_str}")
            self.cursor.execute(query, (numeriai_str, sku_str))
            lp_values = [row.LP for row in self.cursor.fetchall()]
            print(f"Fetched LP values: {lp_values}")
            return lp_values
        except pyodbc.Error as e:
            print(f"Error fetching LP values: {e}")
            return []

    def update_invoice_status(self, symbol):
        print(f"Updating status for invoice with SYMBOL: {symbol}")
        query = "UPDATE dbo.LUZ_Zwroty SET czy_zwrocone = 1 WHERE SYMBOL = ?"
        try:
            self.cursor.execute(query, (symbol,))
            self.conn.commit()
            print(f"Invoice {symbol} status updated to returned.")
        except pyodbc.Error as e:
            print(f"Error updating invoice status: {e}")

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            print("Connection closed")
        except pyodbc.Error as e:
            print(f"Error closing connection: {e}")
