import mysql.connector
from db_table_con import get_connection, create_database_if_not_exists, create_table_if_not_exists


x = ("-" * 50) 

def main_menu():
    """
    Displays the main menu and prompts the user for a choice.
    Returns the user's choice as a string.
    """

    print("Task Manager - Main Menu:\n"
          "1. Add Task\n"
          "2. View Tasks\n"
          "3. Update Task\n"
          "4. Remove Task\n"
          "5. Exit")
    print(x)

    while True:
        choice = input("Select an option (1-5): ").strip()
        if choice in ["1", "2", "3", "4", "5"]:
            break
        else:
            print(x)
            print("⚠️Invalid choice. Please select a valid option.")
            print(x)
    return choice


def add_task():
    """
    Adds a new task to the task list. Prompts the user for task name and description. 
    Ensures that the task name is not empty as well as the description.
    """

    print(x)
    task_name = input("Enter the task name: ").strip()

    while True: 
        if task_name == "":
            print("⚠️ Task name cannot be empty. Please enter a valid name.")
            print(x)
            task_name = input("Enter the task name: ").strip()
            continue
        break
    
    while True:
        task_desc = input("Enter the task description: ").strip()
        if task_desc == "":
            print("⚠️ Task description cannot be empty.")
            print(x)
            continue
        else:
            break   

    conn = get_connection()

    if conn is None:
        print("❌ Failed to connect to the database.")
        return
    
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO task_crud (name, description) VALUES (%s, %s)"
        cursor.execute(sql, (task_name, task_desc))
        conn.commit()

        print(x)
        print(f'✅ Task "{task_name}" added successfully.')
        print(x)

        cursor.execute("SELECT * FROM task_crud WHERE name=%s", (task_name,))
        new_task = cursor.fetchone()
        print(f"📝 ID: {new_task[0]}, Name: {new_task[1]}, | Description: {new_task[2]}, | Status: {new_task[3]}, | Created on: {new_task[4]}")
        print(x)

    except mysql.connector.Error as err:
        print(f"❌Error adding task: {err}")

    finally:
        cursor.close()
        conn.close()


def view_tasks():
    """
    Displays all the tasks in the task list. 
    If there is no task in the list, informs the user that no tasks are available.
    Offers an option to filter and view only active tasks (not started or in process).
    """

    print(x)
    print("📝 View Tasks")
    conn = get_connection()
    if conn is None:
        print("❌ Failed to connect to the database.")
        return
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM task_crud")
        tasks = cursor.fetchall()
        if not tasks:
            print("⚠️ No tasks available.")
            print(x)
        else:
            for task in tasks:
                print(f"📝 ID: {task[0]}, Name: {task[1]}, | Description: {task[2]}, | Status: {task[3]}")  

        if not tasks:
            return  
        
        print(x)
        filter_choice = input("Do you want to see only active tasks (not started or in process)? yes/no: ").strip().lower()

        if filter_choice =="no":
            return
        if filter_choice == "yes":
            cursor.execute("SELECT * FROM task_crud WHERE status IN (%s, %s)", ("not started","in process"))
            filtered_tasks = cursor.fetchall()
        if not filtered_tasks:
            print(x)
            print("⚠️ No active tasks available.")
            print(x)
        else:
            print(x)
            print("📋 Active tasks:")
            print(x)
            for task in filtered_tasks:
                print(f"📝 ID: {task[0]}, Name: {task[1]}, | Description: {task[2]}, | Status: {task[3]}")    
        
    except mysql.connector.Error as err:
        print(f"❌ Error retrieving tasks: {err}")

    finally:
        cursor.close()
        conn.close()


def update_task():
    """
    Shows all tasks and options of updating.
    Updates the status of an existing task based on user input.
    If there are no tasks, informs the user that there are no tasks to update.
    """

    conn = get_connection()

    if conn is None:
        print("❌ Failed to connect to the database.")
        return
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name, status FROM task_crud")
        tasks = cursor.fetchall()
        if not tasks:
            print(x)
            print("⚠️ No tasks available.")
            print(x)
            return
        else:
            for task in tasks:
                print(f"📝 ID: {task[0]}, Name: {task[1]}, | Status: {task[2]}")

    except mysql.connector.Error as err:
        print(f"❌ Error retrieving tasks: {err}")
        return
    
    while True:
        task_id = input("Enter the ID of the task you want to update: ").strip()
        print(x)
        if not task_id.isdigit():
            print("⚠️ Invalid task ID. Enter a number.")
            continue

        cursor.execute("SELECT * FROM task_crud WHERE id=%s", (task_id,))
        task = cursor.fetchone()

        if task:
            break
        else:
            print(x)
            print("⚠️ No task found with that ID. Try again.")

    while True:
        new_status = input("Enter the new status:\n"
          "1. in process\n"
          "2. done\n").strip()
        print(x)
    
        if new_status == "1":
            new_status = "in process"
            break
        elif new_status == "2":
            new_status = "done"
            break
        else:
            print("⚠️ Invalid status choice. Please try again.")
            print(x)
            
    try:
        cursor.execute("UPDATE task_crud SET status = %s WHERE id = %s", (new_status, task_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"✅ Task with ID {task_id} updated successfully.")
        else:
            print(f"⚠️ No task found with ID {task_id}.")

        cursor.execute("SELECT id, name, status FROM task_crud WHERE id=%s", (task_id,))
        updated_task = cursor.fetchone()
        print(f"🔄 Updated Task -> ID: {updated_task[0]}, Name: {updated_task[1]}, | Status: {updated_task[2]}")
        print(x)

    except mysql.connector.Error as err:
        print(f"❌ Error updating task: {err}")

    finally:
        cursor.close()
        conn.close()


def remove_task():
    """
    Removes a task from the task list based on user input.
    If there are no tasks, informs the user that there are no tasks to remove.
    Handles invalid input such as non-numeric values or numbers outside the valid range.
    """

    conn = get_connection()

    if conn is None:
        print("❌ Failed to connect to the database.")
        return
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name FROM task_crud")
        tasks = cursor.fetchall()
        if not tasks:
            print("⚠️ No tasks to remove.")
            print(x)
            return
        
        for task in tasks:
            print(f"📝 ID: {task[0]}, Name: {task[1]}")

        while True:
            task_id = input("Enter the ID of the task to remove: ").strip()
            if not task_id.isdigit():
                print(x)
                print("⚠️ Invalid task ID. Please enter a number.")
                print(x)
                continue

            try:
                cursor.execute("DELETE FROM task_crud WHERE id = %s", (task_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    print(x)
                    print(f'✅ Task with ID "{task_id}" removed successfully.')
                    break
                else:
                    print(x)
                    print("⚠️ No task found with that ID. Please try again.")

            except mysql.connector.Error as err:
                print(f"❌ Error removing task: {err}")
    
    finally:
        cursor.close()
        conn.close()

    print(x)


if __name__ == "__main__":
    print(x)
    print("👋 Welcome to Task Manager!")
    print(x)

    create_database_if_not_exists()
    create_table_if_not_exists()


    while True:
        user_choice = main_menu()

        if user_choice == "1":
            add_task()

        elif user_choice == "2":
            view_tasks()

        elif user_choice == "3":
            update_task() 

        elif user_choice == "4":
            remove_task()

        elif user_choice == "5":
            print(x)
            print("👋 Exiting Task Manager. Goodbye!")

            break
