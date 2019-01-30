"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_all_grades(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects = projects)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-creation")
def make_new_student():
    """Create a new student."""

    return render_template("student_creation.html")


@app.route("/student-add", methods=['POST'])
def add_student():
    """Add a student."""

    first = request.form.get('first_name')
    last = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first, last, github)

    return render_template("student_added.html", github = github)


@app.route("/project")
def show_project():
    """Show information about a project"""

    project = request.args.get('project')
    project_info = hackbright.get_project_by_title(project)
    

    return render_template("project_info.html", title=project_info[0],
                            description=project_info[1], max_grade=project_info[2])




if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
