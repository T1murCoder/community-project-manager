from flask import Blueprint, render_template, abort, request, url_for, redirect
from flask_login import login_required, current_user
from data import db_session
from data.users import User
from data.projects import Project


views = Blueprint("views", __name__, template_folder="../templates", static_url_path="../static")


@views.route("/")
@views.route("/home")
def home():
    
    db_sess = db_session.create_session()
    projects = db_sess.query(Project).all()

    return render_template("home.html", title='Home', projects=projects, user=current_user)


def create_project():
    pass

@views.route("/join-project/<int:project_id>")
@login_required
def join_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    user = db_sess.query(User).get(current_user.id)
    
    if user in project.members:
        abort(404)
    
    project.add_member(user)
    db_sess.commit()

    return redirect(url_for("views.home"))


def leave_project():
    pass