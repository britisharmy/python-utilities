import mysql.connector
from mysql.connector import Error
import threading

# Database configuration
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

# Function to export table schema
def export_table_schema(table_name):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Get table schema
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            table_schema = cursor.fetchone()[1]

            # Write table creation statement to the file
            with open('exported.sql', 'a') as file:
                file.write(f"{table_schema};\n\n")

            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error exporting schema for table {table_name}: {e}")
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to export table data
def export_table_data(table_name):
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Fetch all data from the table
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()

            # Write data insert statements to the file
            with open('exported.sql', 'a') as file:
                file.write(f"INSERT INTO {table_name} VALUES\n")
                for row in table_data:
                    file.write(str(row) + ",\n")
                file.write(";\n\n")

            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error exporting data for table {table_name}: {e}")
        if connection.is_connected():
            cursor.close()
            connection.close()

# Function to export all tables using multithreading
def export_all_tables():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            cursor = connection.cursor()

            # Get all table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            threads = []
            for table in tables:
                table_name = table[0]
                thread_schema = threading.Thread(target=export_table_schema, args=(table_name,))
                thread_data = threading.Thread(target=export_table_data, args=(table_name,))
                threads.extend([thread_schema, thread_data])
                thread_schema.start()
                thread_data.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            cursor.close()
            connection.close()
    except Error as e:
        print(f"Error connecting to database: {e}")
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    export_all_tables()
    print("Export completed. Check exported.sql for the exported schema and data.")
