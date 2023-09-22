# TASK MANAGER
#### Video Demo:https://youtu.be/fiP3P5bO6Dg
#### Description:
The provided code represents a Flask-based web application called "Task Manager." It allows users to register, log in, and manage their tasks. Here is an overview of the functionality and structure of the application:

1. **Files and Functionality**:
   - `application.py`: Contains the main Flask application logic, including route handling and request processing.
   - `helpers.py`: Contains helper functions used in the application, such as the `login_required` decorator and the `apology` function for displaying error messages.
   - `templates/`: Folder containing HTML templates for rendering different web pages.
   - `static/`: Folder containing static files like CSS stylesheets and JavaScript files.

2. **Design Choices**:
   - **Session Management**: The application uses Flask-Session to handle session management. Session data is used to store the user's login status and user ID, allowing authentication and retrieval of user-specific data.
   - **Database**: SQLite is used as the database for storing task information and user credentials. The `tasks.db` file stores tables for tasks and users. The application interacts with the database using the CS50 library to execute SQL queries.
   - **Registration and Login**: Users can register a new account by providing a unique username and password. The password is securely hashed using the `generate_password_hash` function from the `werkzeug.security` module. During login, the provided password is checked against the stored hashed password using the `check_password_hash` function.
   - **Task Management**: Users can create new tasks by providing details such as start date, due date, task name, description, and status. Tasks are stored in the `new_task` table in the database. Users can view their tasks on the homepage, mark tasks as completed, and remove tasks from their task list.
   - **Task Categorization**: Tasks can be categorized into different status categories like "Pending" and "Completed." Users can filter their tasks based on these categories using the corresponding routes.
   - **Flash Messages**: Flash messages are used to display success and error messages to the user, providing feedback on actions like adding tasks or invalid login attempts.

3. **Conclusion**:
   The Flask Task Manager provides a user-friendly interface for managing tasks effectively. It leverages Flask's capabilities for web development and integrates SQLite for data storage. Users can register, log in, create tasks, track task progress, and categorize tasks based on status. The application aims to enhance task organization and productivity.