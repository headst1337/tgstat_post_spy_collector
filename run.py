from app import create_app, db
from app.models.user import User
from app.config import Config


app = create_app()

if __name__ == '__main__':
    with app.app_context():
        user = User.query.filter_by(username='admin').first()
        if user is None:
            new_user = User(username=Config.ADMIN_USERNAME, password=Config.ADMIN_PASSWORD)
            db.session.add(new_user)
            db.session.commit()

    app.run(host='0.0.0.0', port=5000, debug=True)
