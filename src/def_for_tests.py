import mysql.connector

def add_task_to_db(name, description, database="task_test_db"):
    if not name or not description:
        return False

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="zzjezivot",
            database=database
        )

        cursor = conn.cursor()
        sql = "INSERT INTO task_crud (name, description) VALUES (%s, %s)"
        cursor.execute(sql, (name, description))
        conn.commit()
        return True
    
    except mysql.connector.Error:
        return False
    
    finally:
        cursor.close()
        conn.close()


def update_task_status(task_id, status, database="task_test_db"):
    if status not in ['not started', 'in process', 'done']:
        return False

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="zzjezivot",
            database=database
        )

        cursor = conn.cursor()
        sql = "UPDATE task_crud SET status = %s WHERE id = %s"
        cursor.execute(sql, (status, task_id))
        conn.commit()
        return cursor.rowcount > 0
    
    except mysql.connector.Error:
        return False
    
    finally:
        cursor.close()
        conn.close()


def remove_task_from_db(task_id, database="task_test_db"):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",    
            password="zzjezivot",
            database=database
        )
        cursor = conn.cursor()
        sql = "DELETE FROM task_crud WHERE id = %s"
        cursor.execute(sql, (task_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    except mysql.connector.Error:
        return False
    finally:
        cursor.close()
        conn.close()
        