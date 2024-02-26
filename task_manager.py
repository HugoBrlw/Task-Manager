"""
A simple task manager app demonstrating writing and reading from files
"""


#=====importing libraries===========
from datetime import date, datetime

import string

import re

import os

#====Login Section====
# Login page includes menu
          
def login_page():
    name1 = input("Please enter username: ")
    password1 = input("Please enter password: ")
    found = False

    with open("user.txt", "r") as file:
        for line in file:
            field = line.split(", ") # Ensure that username and password are stored separately
            username = field[0]
            password = field[1].strip()  # remove trailing newline

            # Compare to see if the inputs match users.txt
            if name1 == username and password1 == password:
                print("Welcome,", username)
                found = True
                break

    if found:
    # Show menu only if login was successful
    # Check if user is admin
        is_admin = name1 =="admin"
        
        # Show menu for admin 
        # Manage users function not included. Admins have access to user.txt
        while True:
            if is_admin:
                menu = input('''Select one of the following options:
                    r - register a user
                    a - add task
                    va - view all tasks
                    vm - view my tasks
                    s - view statistics
                    e - exit
                    : ''').lower()
            
            # For non-admins
            else:
                menu = input('''Select one of the following options:
                    a - add task
                    va - view all tasks
                    vm - view my tasks
                    e - exit
                    : ''').lower()
        
        
        # Process menu selection
            
            if menu in ['r', 'a', 'va', 'vm', 's', 'e']:
                # Ensure only admins can register users
                if menu == 'r' and is_admin:
                    register_user()                                    

                elif menu == 'a':
                    add_task()
                    due_date()
                    task_progress()
                    print("\nTask added successfully!\n")

                elif menu == 'va':
                    view_all()

                elif menu == 'vm':
                    # Ensure logged in user gets their tasks
                    logged_in_username = name1
                    view_my(logged_in_username)
                
                # Ensure that s is not a hidden option for non-admins by adding is_admin
                elif menu == 's' and is_admin:
                    view_statistics()

                elif menu == 'e':
                    print('Goodbye!!!')
                    exit()

                else:
                    print("You have made entered an invalid input. Please try again.")
                    
    else:
    # If no match is found
        print("Incorrect username or password. Try again or contact the administrator to change password or register.")
        login_page()

#====r - Register user / User Data====
# Save password and user in user.txt
def register_user():
    existing_users = set()
    with open("user.txt", "r") as file:
        for line in file:
            existing_users.add(line.strip().split(',')[0]) # Prime existing users

    # Get valid usernames and check that they are available for use
    valid_username = False
    while not valid_username:
        user = input("Please enter a new username: ").strip() # Add strip() to remove whitespace
        
        if not user: # Check if username empty
            print("Username cannot be blank. Please try again.")
            continue

        if user not in existing_users:
            valid_username = True
        else:
            print("Username already taken. Please try another.")

    while True:
        password = input("Please enter your password: ")
        if len(password) < 6:
            print("Password must be at least six characters.")
            continue

        # Password complexity 
        has_special_char = False
        has_number = False
        has_capital = False
        has_lower = False

        for char in password:
            if char in string.punctuation:
                has_special_char = True
            elif char.isdigit():
                has_number = True
            elif char.isupper():
                has_capital = True
            elif char.islower():
                has_lower = True

        if not (has_special_char and has_number and has_capital):
            print("Password must contain at least one special character, one number, and one capital letter.")
            continue


        # Verify and compare passwords
        password_verify = input("Please re-enter your password: ")

        if password == password_verify:
            with open("user.txt", "a+") as file:
                file.write(user + ", " + password + "\n")
            print("User added successfully!")
            break
        else:
            print("Password do not match. Please try again.")

#====a - Adding New Tasks====
       
# Define the add task function
def add_task():
  with open("tasks.txt", "a+") as tasks_file, open("user.txt") as users_file:
    task_title = input("Please enter the title of the task: ")

    # Extract usernames from the user file
    usernames = []
    for line in users_file.read().splitlines():
      username = re.search(r"^[^,]+", line)  # Take everything before the comma
      if username:
        usernames.append(username.group(0))

    # Check if the assigned username exists in the user list
    assigned_to = None
    while not assigned_to:
      assigned_to = input("Please enter the username of the person whom the task is assigned to: ")
      if assigned_to not in usernames:
        print("That username is not registered.")
        print("Registered users:")
        for user in usernames:
          print(user)
        assigned_to = None  # Reset assigned_to to continue the loop

    # Get the task description and date assigned
    task_descr = input("Please provide a description of the task: ")
    date_assigned = datetime.today()

    # Format the task entry and write it to the file
    tasks_file.write(f"\nTask:\t\t\t{task_title}\n")
    tasks_file.write(f"Assigned to:\t{assigned_to}\n")
    tasks_file.write(f"Date Assigned:\t{str(date_assigned)}\n")
    tasks_file.write(f"Description:\t{task_descr}\n")

# Configure due_date to accept valid input only
def due_date():
    with open("tasks.txt", "a+") as file:
        while True:
            task_due_date_str = input("Please enter the due date of the task (YYYY-MM-DD): ")
            try:
                task_due_date = date.fromisoformat(task_due_date_str)
            except ValueError:
                print(f"Invalid date format. Please enter the date in YYYY-MM-DD format.")
                continue

            today = date.today()

            if task_due_date >= today:
                file.write(f"Due Date:\t\t{task_due_date.strftime('%Y-%m-%d')}\n")
                break
            else:
                print("That date is already past.")
                continue
  
# Track task progress
def task_progress():
    with open("tasks.txt", "a+") as file:
        while True:
            task_progress = input("Type 'yes' if the task has been completed, else leave blank: ")

            if task_progress.lower() == 'yes':
                file.write("Task Complete:\t" + "Yes\n")
                break

            elif task_progress == '':
                file.write("Task Complete:\t" + "No\n")
                break

            else:
                print("You have entered an invalid input. Please try again.")

#====va - View All====

def view_all():
  
  with open("tasks.txt", "r") as file:
    # Read all lines from the file
    lines = file.read()
    print(lines.expandtabs(4)) # To ensure output is same as in file

#====vm - View My Tasks====

def view_my(logged_in_username):
    file = "tasks.txt"
    assignment = logged_in_username
    with open("tasks.txt", "r") as file:
        text = file.read()
        paragraphs = text.split("\n\n")  # Split by empty lines

        for paragraph in paragraphs:
            if assignment in paragraph:
                print(paragraph.expandtabs(4) + "\n")

#====s - View Statistics====

def view_statistics():
    try:
        with open("tasks.txt", "r") as tasks_file, open("user.txt") as users_file:
            # Total tasks
            task_data = tasks_file.read()
            task_count = task_data.count("Task:")
            print(f"Total tasks: {task_count}")

            # Total users
            tot_users = len(users_file.readlines())
            print("Total users:", tot_users)



    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}")

#====Complete Program====

# Initialise admin account in user.txt for first use of program and create tasks.txt
admin_data = "user.txt"
admin_username = "admin"
admin_password = "adm1n"

if not os.path.exists(admin_data):
    with open("user.txt", "a+") as initial, open("tasks.txt", "a") as initial2:
        initial.write(admin_username + ", " + admin_password + "\n") # \n to ensure registering a user occurs in new line
    print(f"Admin account created as user: {admin_username}, and password: {admin_password}")

# Actual program
login_page()
