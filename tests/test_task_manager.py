import pytest
from src.def_for_tests import add_task_to_db, update_task_status, remove_task_from_db
from tests.test_db import setup_test_db, get_connection


# =========================== AD TASK TESTS ===========================

def test_add_task_success(setup_test_db):
    """
    Test for successful addition of a task.
    verfies that the task with name and description is added to the database.
    """

    task_name = "Test task"
    task_desc = "Test description"
    result = add_task_to_db(task_name, task_desc)
    assert result is True

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM task_crud WHERE name = %s", (task_name,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    assert task is not None
    assert task[0] == task_name
    assert task[1] == task_desc

def test_add_task_empty_name(setup_test_db):
    """
    Negative test for adding a task with an empty name.
    Ensures that a task with an empty name is not added to the database.
    """

    task_name = ""
    task_desc = "Test description"
    result = add_task_to_db(task_name, task_desc)
    assert result is False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM task_crud WHERE description = %s", (task_desc,))
    tasks = cursor.fetchone()
    cursor.close()
    conn.close()
    assert not tasks


# =========================== UPDATE TASK TESTS ===========================

def test_update_task_status_success(setup_test_db):
    """
    Test for successful update of a task's status.
    Adds a task, updates its status, and verifies the update in the database.
    """

    task_name = "Task to update"
    task_desc = "Description"
    add_task_to_db(task_name, task_desc)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM task_crud WHERE name = %s", (task_name,))
    task = cursor.fetchone()
    task_id = task[0]
    cursor.close()
    conn.close()

    new_status = "in process"
    result = update_task_status(task_id, new_status)
    assert result is True

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM task_crud WHERE id = %s", (task_id,))
    updated_task = cursor.fetchone()
    cursor.close()
    conn.close()
    assert updated_task[0] == new_status


def test_update_task_status_failure(setup_test_db):
    """
    Negative test for updating a task's status with an invalid task ID.
    Attempts to update the status of a non-existent task and verifies that the update fails.
    """

    invalid_task_id = 5478
    new_status = "done"
    result = update_task_status(invalid_task_id, new_status)
    assert result is False

    conn = get_connection()
    cursor = conn.cursor()  
    cursor.execute("SELECT status FROM task_crud WHERE id = %s", (invalid_task_id,))
    task = cursor.fetchone()    
    cursor.close()
    conn.close()
    assert task is None


# =========================== REMOVE TASK TESTS ===========================

def test_remove_task_success(setup_test_db):
    """
    Test for successful removal of a task.
    Adds a task, removes it, and verifies that it no longer exists in the database.
    """

    task_name = "Task to remove"
    task_desc = "Description"
    add_task_to_db(task_name, task_desc)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM task_crud WHERE name = %s", (task_name,))
    task = cursor.fetchone()
    task_id = task[0]
    cursor.close()
    conn.close()

    result = remove_task_from_db(task_id)
    assert result is True

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM task_crud WHERE id = %s", (task_id,))
    removed_task = cursor.fetchone()
    cursor.close()
    conn.close()
    assert removed_task is None


def test_remove_task_failure(setup_test_db):
    """
    Negative test for removing a task with an invalid task ID.
    Attempts to remove a non-existent task and verifies that the removal fails.
    """

    invalid_task_id = 1
    result = remove_task_from_db(invalid_task_id)
    assert result is False

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM task_crud WHERE id = %s", (invalid_task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    assert task is None


