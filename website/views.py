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
    
    return render_template("create_project.html", page_header="Создание проекта", form=form, user=current_user)    


@views.route("/join-project/<int:project_id>")
@login_required
def join_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    user = db_sess.query(User).get(current_user.id)
    
    if not project:
        abort(404)
    
    if user in project.members or len(project.members) == project.max_members:
        abort(404)
    
    project.add_member(user)
    db_sess.commit()

    return redirect(url_for("views.home"))


@views.route("/leave-project/<int:project_id>")
def leave_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    
    if not project:
        abort(404)
    
    if current_user.id == project.leader_id:
        abort(404)
    
    user = db_sess.query(User).get(current_user.id)
    user.projects.remove(project)
    db_sess.commit()
    return redirect(url_for("views.my_projects"))


@views.route("/delete-project/<int:project_id>")
def delete_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    
    if not project:
        abort(404)
    
    if current_user.id != project.leader_id:
        abort(404)
    
    db_sess.delete(project)
    db_sess.commit()
    return redirect(url_for("views.my_projects"))


@views.route("/my-projects")
@login_required
def my_projects():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    print(user.projects)
    return render_template("my_projects.html", projects=user.projects, user=current_user)


@views.route("/edit-project/<int:project_id>", methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    form = CreateProjectForm()
    
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    user = db_sess.query(User).get(current_user.id)
    
    if not project:
        abort(404)
    
    if user.id != project.leader_id:
        abort(404)
    
    if form.validate_on_submit():
        project.name = form.name.data
        project.max_members = form.max_members.data
        project.description = form.description.data
        
        db_sess.commit()
        return redirect(url_for("views.my_projects"))
    
    form.name.data = project.name
    form.max_members.data = project.max_members
    form.description.data = project.description
    
    return render_template("create_project.html", page_header="Редактирование проекта", form=form, user=current_user)


@views.route("/view-project/<int:project_id>")
@login_required
def view_project(project_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    user = db_sess.query(User).get(current_user.id)
    
    if not project:
        abort(404)
    
    if user not in project.members:
        abort(404)
    
    return render_template("view_project.html", prj=project, user=current_user)


@views.route("/delete-member/<int:project_id>/<int:member_id>")
@login_required
def delete_member(project_id, member_id):
    db_sess = db_session.create_session()
    project = db_sess.query(Project).get(project_id)
    member = db_sess.query(User).get(member_id)
    user = db_sess.query(User).get(current_user.id)
    
    if not project or not member:
        abort(404)
    
    if member.id == user.id:
        abort(404)
    
    if user.id != project.leader_id:
        abort(404)
    
    if member not in project.members:
        abort(404)
    
    project.members.remove(member)
    db_sess.commit()
    
    return redirect(url_for("views.view_project", project_id=project_id))