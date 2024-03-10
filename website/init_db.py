from website import create_app
from website.models import User, ReportInfo, db
from werkzeug.security import generate_password_hash


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()

        if User.query.count() == 0:
            hashed_password = generate_password_hash("lalala")
            new_user = User(id=1, student_id=100744646, email="yomama@hotmail.com", password_hash=hashed_password,
                            first_name="Jane", last_name="Doe", role="Student")
            db.session.add(new_user)
            db.session.commit()


if __name__ == '__main__':
    init_db()
