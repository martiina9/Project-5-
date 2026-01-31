import mysql.connector
import pytest

def create_test_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="zzjezivot"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_test_db")
    cursor.close()
    conn.close()


def get_connection(database="task_test_db"):
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="zzjezivot",
            database=database
        )
        return conn
    

def create_test_table():
    conn = get_connection()    
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_crud (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            status ENUM('not started', 'in process', 'done') DEFAULT 'not started',
            created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.execute("TRUNCATE TABLE task_crud")
    conn.commit()
           
    cursor.close()



@pytest.fixture(scope="function")
def setup_test_db():
    # Setup: vytvořit testovací DB a tabulku
    create_test_database()
    create_test_table()
    yield  # tady běží test
    # Teardown: po testu tabulku vyprázdnit

