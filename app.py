import streamlit as st
import sqlite3
import pandas as pd

# Database setup
def create_table():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, task TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def add_task(task, status="ongoing"):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, status))
    conn.commit()
    conn.close()

def get_tasks(status):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM tasks WHERE status=?", (status,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_all_tasks(status):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE status=?", (status,))
    conn.commit()
    conn.close()

# Initialize database
create_table()

# Streamlit app
st.title("📋 Task Manager")

# Add space between the title and content
st.markdown("---")

# Manage task lists in session state to dynamically update UI
if 'ongoing_tasks' not in st.session_state:
    st.session_state.ongoing_tasks = get_tasks("ongoing")
if 'done_tasks' not in st.session_state:
    st.session_state.done_tasks = get_tasks("done")

# Create adjacent columns for desktop, and let Streamlit handle responsive stacking for mobile
col1, col2 = st.columns([1, 1], gap="large")

# Column 1: Ongoing Tasks
with col1:
    st.subheader("🟡 Ongoing Tasks")
    
    # Display existing ongoing tasks
    ongoing_tasks = st.session_state.ongoing_tasks
    
    if ongoing_tasks:
        for task_id, task_name in ongoing_tasks:
            col_ongoing_1, col_ongoing_2, col_ongoing_3 = st.columns([4, 1, 1])
            with col_ongoing_1:
                st.write(f"• {task_name}")
            with col_ongoing_2:
                if st.button("✅", key=f"complete_{task_id}"):
                    complete_task(task_id)
                    # Update the session state directly after task completion
                    st.session_state.ongoing_tasks = get_tasks("ongoing")
                    st.session_state.done_tasks = get_tasks("done")
            with col_ongoing_3:
                if st.button("🗑️", key=f"delete_ongoing_{task_id}"):
                    delete_task(task_id)
                    # Update the session state after deleting the task
                    st.session_state.ongoing_tasks = get_tasks("ongoing")
    else:
        st.write("No ongoing tasks!")

    # Add a new task
    st.markdown("---")
    st.subheader("➕ Add a New Task")
    new_task = st.text_input("Task Name", placeholder="Enter your task here...")
    if st.button("Add Task"):
        if new_task.strip():
            add_task(new_task)
            # Update session state after adding task
            st.session_state.ongoing_tasks = get_tasks("ongoing")

    # Add a button to delete all ongoing tasks
    if st.button("❌ Delete All Ongoing Tasks"):
        delete_all_tasks("ongoing")
        st.session_state.ongoing_tasks = get_tasks("ongoing")

# Column 2: Done Tasks
with col2:
    st.subheader("✅ Done Tasks")

    # Display completed tasks
    done_tasks = st.session_state.done_tasks
    
    if done_tasks:
        for task_id, task_name in done_tasks:
            col_done_1, col_done_2 = st.columns([4, 1])
            with col_done_1:
                st.write(f"• {task_name}")
            with col_done_2:
                if st.button("🗑️", key=f"delete_done_{task_id}"):
                    delete_task(task_id)
                    # Update the session state after deleting the task
                    st.session_state.done_tasks = get_tasks("done")
    else:
        st.write("No tasks completed yet!")

    # Add a button to delete all done tasks
    if st.button("❌ Delete All Done Tasks"):
        delete_all_tasks("done")
        st.session_state.done_tasks = get_tasks("done")

# Adding spacing and separator for better UI
st.markdown("---")
st.write("Task Manager © 2024")
