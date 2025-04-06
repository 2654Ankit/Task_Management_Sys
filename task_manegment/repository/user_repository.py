from Models.User import Users
from extensions import db

class UserRepository:
    def get_by_username(self, username):
        return Users.query.filter_by(username=username).first()

    def add_user(self, username, password, role):
        user = Users(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
