from flask import Blueprint, render_template
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