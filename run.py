from app import create_app, db
from app.models.user import User

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if user is None:
            new_user = User(username='admin', password='password')
            db.session.add(new_user)
            db.session.commit()
