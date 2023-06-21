from flask import render_template, redirect, send_file, url_for, flash
from flask_login import login_required, current_user

from . import bp
from app.models.post import Post
from app import db
from app.utils import generate_csv_report, generate_excel_report

from flask import request
from datetime import datetime

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    filter = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)  # Get the current page number from the request arguments
    posts = []

    if filter == 'pagination':
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=10)  # Display 10 posts per page
    elif filter == 'calendar':
        date_str = request.args.get('date')
        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                posts = Post.query.filter(db.func.date(Post.timestamp) == date).order_by(Post.timestamp.desc()).paginate(page=page, per_page=10)
            except ValueError:
                flash('Invalid date format.', 'error')
        else:
            flash('Please select a date.', 'error')
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=1)

    return render_template('dashboard.html', posts=posts, filter=filter)
