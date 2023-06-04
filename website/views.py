from flask import Blueprint, render_template, abort, request, url_for, redirect
from flask_login import login_required, current_user
from data import db_session
from data.users import User
from data.projects import Project
from .forms.CreateProjectForm import CreateProjectForm


views = Blueprint("views", __name__, template_folder="../templates")


@views.route("/")
@views.route("/home")
def home():
    db_sess = db_session.create_session()
    projects = db_sess.query(Project).all()

    return render_template("home.html", title='Home', projects=projects, user=current_user)

@views.route("/create-project", methods=['GET', 'POST'])
@login_required
def create_project():
    form = CreateProjectForm()
    
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        
        project = Project(
            name=form.name.data,
            max_members=form.max_members.data,
            description=form.description.data
        )
        project.set_leader(user)
        
        db_sess.add(project)
        db_sess.commit()
        
        return redirect(url_for("views.home"))
    
    return render_template("create_project.html", form=form, user=current_user)    


@views.route("/join-project/<int:project_id>")
@login_required
def join_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    user = db_sess.query(User).get(current_user.id)
    
    if user in project.members or len(project.members) == project.max_members:
        abort(404)
    
    project.add_member(user)
    db_sess.commit()

    return redirect(url_for("views.home"))


def leave_project():
    pass


def delete_project():
    pass


@views.route("/my-projects")
@login_required
def my_projects():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    
    return render_template("my_projects.html", projects=user.projects, user=current_user)