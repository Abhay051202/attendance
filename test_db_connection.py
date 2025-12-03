import mysql.connector
from mysql.connector import errorcode
from config.config import MYSQL_CONFIG

def test_connection():
    print("Testing connection with config:")
    print(f"Host: {MYSQL_CONFIG['host']}")
    print(f"User: {MYSQL_CONFIG['user']}")
    print(f"Port: {MYSQL_CONFIG['port']}")
    
    try:
        # Try connecting to the specific database
        print(f"Attempting to connect to database '{MYSQL_CONFIG['database']}'...")
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        print("SUCCESS: Connected to database 'demo'!")
        conn.close()
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database 'demo' does not exist. Attempting to create it...")
            try:
                # Connect without database to create it
                temp_config = MYSQL_CONFIG.copy()
                if 'database' in temp_config:
                    del temp_config['database']
                
                conn = mysql.connector.connect(**temp_config)
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE {MYSQL_CONFIG['database']}")
                print(f"SUCCESS: Database '{MYSQL_CONFIG['database']}' created!")
                conn.close()
                return True
            except mysql.connector.Error as err2:
                print(f"FAILED to create database: {err2}")
                return False
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
             print("FAILED: Access denied. Wrong username or password.")
             return False
        else:
            print(f"FAILED: {err}")
            return False

if __name__ == "__main__":
    test_connection()
