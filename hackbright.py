"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print("Student: {} {}\nGitHub account: {}".format(row[0], row[1], row[2]))

    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO students (first_name, last_name, github)
          VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name,
                               'last_name': last_name,
                               'github': github})
    db.session.commit()

    print("Successfully added student: {} {}".format(first_name, last_name))


def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """
        SELECT title, description, max_grade
        FROM projects
        WHERE title = :title
    """

    db_cursor = db.session.execute(QUERY, {'title': title})

    row = db_cursor.fetchone()

    print("Project Title: {}\nDescription: {}\nMax Grade: {}".format(row[0], row[1], row[2]))

    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """
        SELECT grade
        FROM grades
        WHERE student_github = :github 
            AND project_title = :title
    """

    db_cursor = db.session.execute(QUERY, {'github':github, 'title':title})

    row = db_cursor.fetchone()

    print("{} got {} on their project {}".format(github, row[0], title))


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    
    QUERY = """
        INSERT INTO grades (student_github, project_title, grade)
            VALUES (:student_github, :project_title, :grade)
    """

    db.session.execute(QUERY, {'student_github': github,
                               'project_title': title,
                               'grade': grade})

    db.session.commit()

    print("Successfully added a grade: {} got {} on their project {}".format(github, grade, title))

def make_new_project(title, max_grade, description):
    """Add a project and print confirmation.

    Given a title, max grade, and description, add project to the
    database and print a confirmation message.
    """

    QUERY = """
        INSERT INTO projects (title, max_grade, description)
          VALUES (:title, :max_grade, :description)
        """

    db.session.execute(QUERY, {'title': title,
                               'max_grade': max_grade,
                               'description': description})
    db.session.commit()

    print("Successfully added project")


def get_all_grades_for_student(student_github):
    """Print grade student received for a project."""
    
    QUERY = """
        SELECT project_title, grade
        FROM grades
        WHERE student_github = :github 
    """

    db_cursor = db.session.execute(QUERY, {'github': student_github})

    rows = db_cursor.fetchall()

    for row in rows:
        print("{} got {} on their project {}".format(student_github, row[1], row[0]))

    return rows


def get_all_grades(title):
    """Print all grades for a project."""
    
    QUERY = """
        SELECT student_github, grade
        FROM grades
        WHERE project_title = :title
    """

    db_cursor = db.session.execute(QUERY, {'title': title})

    rows = db_cursor.fetchall()

    return rows

def get_all_students_and_projects():
    """Get all enlisted students."""
    
    STUDENT_QUERY = """
        SELECT github
        FROM students
    """

    PROJECT_QUERY = """
        SELECT title
        FROM projects
    """

    db_cursor1 = db.session.execute(STUDENT_QUERY)
    db_cursor2 = db.session.execute(PROJECT_QUERY)

    student_rows = db_cursor1.fetchall()
    project_rows = db_cursor2.fetchall()

    return student_rows, project_rows


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "get_project":
            title = args[0]
            get_project_by_title(title)

        elif command == "get_grade":
            github, title = args  # unpack!
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args  # unpack!
            assign_grade(github, title, grade)

        elif command == "new_project":
            title, max_grade = args[0],args[1]
            description = " ".join(args[2:])
            make_new_project(title, max_grade, description)

        elif command == "get_all_grades":
            student_github = args[0]
            get_all_grades_for_student(student_github)

        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
