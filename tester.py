class DatabaseConnector:
    # ... existing methods ...

    def fetch_orders(self, limit=15):
        query = f"SELECT TOP {limit} PELNY_NR_U_DOST FROM dbo.ZS_NIEOBSLUZONE"
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [row.PELNY_NR_U_DOST for row in rows]
        except pyodbc.Error as e:
            print(f"Error fetching symbols: {e}")
            return []


orders = db.fetch_orders(limit=15)