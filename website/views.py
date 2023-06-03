from flask import Blueprint, render_template
from data import db_session
from data.users import User


views = Blueprint("views", __name__, template_folder="../templates", static_url_path="../static")


@views.route("/")
@views.route("/home")
def home():
    
    return "lol"