from flask import Blueprint, render_template, redirect, url_for, abort, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from .forms.LoginForm import LoginForm
from .forms.RegisterForm import RegisterForm
from data import db_session
from data.users import User


auth = Blueprint("auth", __name__, template_folder="../templates")


# Авторизация
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        abort(404)
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            current_app.logger.info(f"User has logged in: {current_user}")
            flash("Вы вошли в аккаунт!", category="success")
            return redirect(url_for('views.home'))
        flash("Неправильный логин или пароль.", category="error")
    return render_template("login.html", title='Авторизация', form=form, user=current_user)


# Регистрация
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if not current_user.is_anonymous:
        abort(404)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            flash("Пароли не совпадают!", "warning")
            return render_template("signup.html", title='Регистрация', form=form, user=current_user)
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            flash("Такой пользователь уже есть!", "warning")
            return render_template("signup.html", title='Регистрация', form=form, user=current_user)
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        current_app.logger.info(f"New user has registered: {user}")
        flash("Вы зарегистрированы!", "success")
        return redirect(url_for('auth.login'))
    return render_template("signup.html", title='Регистрация', form=form, user=current_user)


# Выход из аккаунта
@auth.route('/logout')
@login_required
def logout():
    current_app.logger.info(f"User logged out: {current_user}")
    logout_user()
    flash("Вы вышли из аккаунта")
    return redirect("/")