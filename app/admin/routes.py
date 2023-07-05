from flask import render_template, redirect, url_for, flash, make_response, request
from flask_login import login_required
from io import BytesIO
from datetime import datetime

from . import bp
from app.models.post import Post
from app import db
from app.utils import generate_excel_report


@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    posts = []
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            posts = Post.query.filter(db.func.DATE(Post.timestamp) == date).order_by(Post.timestamp.desc())
        except ValueError:
            flash('Invalid date format.', 'error')
    else:
        flash('Please select a date.', 'error')

    return render_template('dashboard.html', posts=posts)

@bp.route('/download', methods=['GET'])
@login_required
def download():
    date_str = request.args.get('date')
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            posts = Post.query.filter(db.func.DATE(Post.timestamp) == date).order_by(Post.timestamp.desc()).all()
            output = generate_excel_report(posts) 
            response = make_response(output.getvalue())
            response.headers['Content-Disposition'] = f'attachment; filename=posts_{date}.xlsx'
            response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return response
        except ValueError:
            flash('Invalid date format.', 'error')
    else:
        flash('Please select a date.', 'error')

    return redirect(url_for('admin.dashboard'))
