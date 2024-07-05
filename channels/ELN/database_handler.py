import mysql.connector

class DatabaseHandler:
    def __init__(self, user, password, host, database):
        self.cnx = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
        self.cursor = self.cnx.cursor()

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return str(result[0]) if result else "No results found."
        except Exception as e:
            return f"Error executing query: {e}"

    def close(self):
        self.cursor.close()
        self.cnx.close()