"""
This module contains the main application logic for XYZ application.

The XYZ application is a Flask-based web application that provides various features
such as user authentication, task management, and data storage.

Author: Zohair Abbas
Date: July 16, 2023
"""


# 𝐓𝐀𝐒𝐊 𝐌𝐀𝐍𝐀𝐆𝐄𝐑

from flask import Flask, flash, request, render_template, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from help import login_required, apology

app = Flask(__name__)


# CONFIGURING THE SESSION
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# EXECUTING THE DATABASE
db = SQL("sqlite:///tasks.db")


# INDEX


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        # Get the new status and task ID from the form
        change_status = request.form.get("change_status")
        task_id = request.form.get("task_id")
        if not change_status:
            return apology("Please Select the Status you want to Change!")

        # Update the status of the task in the database
        db.execute(
            "UPDATE new_task SET status = ? WHERE id = ?", change_status, task_id
        )

        # Redirect the user back to the index page
        return redirect("/")

    # Retrieve tasks that are not completed for the current user
    TASKS = db.execute(
        "SELECT * FROM new_task WHERE status != 'Completed' AND username = ? ORDER BY timestamp DESC",
        (session["user_id"],),
    )
    # For pending tasks
    pending = db.execute(
        "SELECT COUNT(task) AS pending FROM new_task WHERE status = 'Pending' AND username = ?",
        session["user_id"],
    )[0]
    print(pending["pending"])

    # For completed tasks
    completed = db.execute(
        "SELECT COUNT(task) AS completed FROM new_task WHERE status = 'Completed' AND username = ?",
        session["user_id"],
    )[0]
    print(completed["completed"])

    # For in progress tasks
    in_progress = db.execute(
        "SELECT COUNT(task) AS in_progress FROM new_task WHERE status = 'In Progress' AND username = ?",
        session["user_id"],
    )[0]
    print(in_progress["in_progress"])
    # Render the index.html template and pass the tasks to it
    return render_template(
        "index.html",
        TASKS=TASKS,
        pending=pending["pending"],
        completed=completed["completed"],
        in_progress=in_progress["in_progress"],
    )


# REGISTER


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
        # Retrieve the username, password, and confirmation password from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username:
            return apology("Must provide username", 400)
        if not password:
            return apology("Must provide password", 400)
        if not confirm_password:
            return apology("Please confirm password", 400)
        if password != confirm_password:
            return apology("Passwords do not match")

        # Check if the username already exists in the database
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 0:
            return apology("Username already exists", 400)

        # Hash the user's password
        hashed_value = generate_password_hash(password)
        checking_password = check_password_hash(hashed_value, password)

        # Store the user's information in the database
        storing_info = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_value
        )

        # Retrieve the user's information from the database and set the session user_id
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]

        # Redirect the user to the homepage
        return redirect("/")
    else:
        # If the request method is GET, render the register.html template
        return render_template("register.html")


# LOG IN
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 401)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Render the login.html template
        return render_template("login.html")


# LOG OUT


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# ADD NEW TASK
@app.route("/add_new_task", methods=["GET", "POST"])
@login_required
def add_new_task():
    if request.method == "POST":
        # Retrieve the task details from the form
        start_date = request.form.get("date")
        due_date = request.form.get("due_date")
        task = request.form.get("task")
        description = request.form.get("description")
        status = request.form.get("status")

        if not start_date or not due_date or not task or not description or not status:
            return apology("Must Provide All Fields")

        if start_date > due_date:
            return apology("Due Date Must be Greater or Equal to Start Date of Task")

        # Define the character limit
        character_limit = 500

        # Truncate the description if it exceeds the character limit
        if len(description) > character_limit:
            description = description[:character_limit]
            flash("You have exceeded the character limit (500)")

        # Add task information to the database
        db.execute(
            "INSERT INTO new_task (username, start_date, due_date, task, description, status) VALUES (?, ?, ?, ?, ?, ?)",
            session["user_id"],
            start_date,
            due_date,
            task,
            description,
            status,
        )

        flash("Successfully Added New Task!")
        return redirect("/")

    # If the request method is GET, render the add_new_task.html template
    return render_template("add_new_task.html")


# REMOVE TASK


@app.route("/remove_task", methods=["GET", "POST"])
@login_required
def remove_task():
    if request.method == "POST":
        # Retrieve the task ID from the form
        task_id = request.form.get("task_id")

        # Delete the task from the database based on the task ID
        db.execute("DELETE FROM new_task WHERE id = ?", task_id)

    # Retrieve all tasks for the current user
    TASKS = db.execute("SELECT * FROM new_task WHERE username = ?", session["user_id"])

    # Render the remove_task.html template and pass the tasks to it
    return render_template("remove_task.html", TASKS=TASKS)


# PENDING TASKS


@app.route("/pending_task")
@login_required
def pending_task():
    # Retrieve pending tasks for the current user
    TASKS = db.execute(
        "SELECT * FROM new_task WHERE username = ? AND status = ?",
        session["user_id"],
        "Pending",
    )

    # Render the pending_task.html template and pass the tasks to it
    return render_template("pending_task.html", TASKS=TASKS)


# COMPLETED TASKS


@app.route("/completed_task")
@login_required
def completed_task():
    # Retrieve completed tasks for the current user
    TASKS = db.execute(
        "SELECT * FROM new_task WHERE username = ? AND status = ?",
        session["user_id"],
        "Completed",
    )

    # Render the completed_task.html template and pass the tasks to it
    return render_template("completed_task.html", TASKS=TASKS)


# ABOUT


@app.route("/about")
@login_required
def about():
    # Render the about.html template
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=False)