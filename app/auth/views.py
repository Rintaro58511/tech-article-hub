from flask import Blueprint, redirect, flash, render_template, url_for
from model import db, User
from flask_login import login_user, logout_user
from forms import SignUpForm, LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')


@auth_bp.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        name = form.user_name.data
        password = form.password.data

        user = User.query.filter_by(user_name = name).first()

        if user and user.check_password(password):

            login_user(user)

            return redirect(url_for("main.get_articles"))
        
        else: flash("認証不備です")

        

    return render_template("auth/login.html", form = form)


@auth_bp.route("/signup", methods = ["GET", "POST"])
def sign_up():
    form = SignUpForm()

    if form.validate_on_submit():
        name = form.user_name.data
        password = form.password.data

        user = User(user_name = name)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("新規登録完了")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/signup.html", form=form)


@auth_bp.route("/logout", methods = ["GET"])
def logout():

    logout_user()
    flash("ログアウトしました")

    return redirect(url_for("auth.login"))
