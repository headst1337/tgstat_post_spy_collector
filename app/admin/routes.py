from flask import render_template, redirect, send_file, url_for, flash
from flask_login import login_required, current_user

from . import bp
from app.models.post import Post
from app import db
from app.utils import generate_csv_report, generate_excel_report


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('admin/dashboard.html', posts=posts)


@bp.route('/report/csv')
@login_required
def report_csv():
    filename = generate_csv_report()
    return send_file(filename)


@bp.route('/report/excel')
@login_required
def report_excel():
    filename = generate_excel_report()
    return send_file(filename)
