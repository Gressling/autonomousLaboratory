# URL to scenario2-DB viewer:   http://gressling.net/AutonomousLaboratory/situation.html 

# ----------------- Imports
import mysql.connector
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

scenario = "CORTEX_" + input("Cortex scenario name: ")

# ----------------- Database Configuration
dbpw = os.getenv('AICHEM_DB_LOGIN')
print(dbpw)

try:
    # Establish connection to the database
    cnx = mysql.connector.connect(
        user='situation', 
        password=dbpw,
        host='den1.mysql6.gear.host',
        database='situation'
    )
    cursor = cnx.cursor()

    # Define the query and values
    query = (
        "INSERT INTO `situation`.`situation2` (`channel`, `prompt`, `comment`) "
        "VALUES (%s, %s, %s);"
    )
    values = ("test", "Hello World", scenario)

    # Execute the query and commit the transaction
    cursor.execute(query, values)
    cnx.commit()
    print("Record inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if cnx:
        cnx.close()
    print("MySQL connection is closed.")
