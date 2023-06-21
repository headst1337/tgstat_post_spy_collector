from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from . import bp
from . forms import LoginForm
from app.models.user import User
from app import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('admin.dashboard'))
    
    return render_template('login.html', title='Sign In', form=form)
