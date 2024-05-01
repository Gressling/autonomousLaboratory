import time
import mysql.connector
from mysql.connector import Error

# Function to create a new database connection
def create_connection():
    return mysql.connector.connect(
        user='situation',
        password=input(),
        host='den1.mysql6.gear.host',
        database='situation'
    )

# SQL query to fetch the latest record
query = "SELECT * FROM situation WHERE pkey = (SELECT MAX(pkey) FROM situation);"

old_row = None
new_row = None

try:
    while True:
        # Rebuild the connection each iteration
        cnx = create_connection()  # Create a new connection
        cursor = cnx.cursor()  # Create a new cursor

        cursor.execute(query)  # Execute the query to fetch the latest record
        result = cursor.fetchone()  # Get the most recent row
        
        if result:  # If a result is found
            new_row = result[0]  # Assuming the first column is the primary key
            if new_row != old_row:  # If the new record is different from the last
                print("New entry:", result)  # Output the new entry
                old_row = new_row  # Update the old_row to the new_row
        else:
            print("No new data found.")  # If there's no new data

        # Close the cursor and connection after each iteration
        cursor.close()  # Properly close the cursor
        cnx.close()  # Properly close the connection

        # Wait before the next check
        time.sleep(2)  # Delay between checks

except Error as e:
    print("An error occurred:", e)  # Handle any database error

