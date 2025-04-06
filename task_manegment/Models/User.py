from extensions import db
from sqlalchemy.sql import func
import enum
from sqlalchemy.orm import relationship
# from Models.Task import TaskManagger

# class role_def(enum.Enum):
#     ADMIN="admin"
#     EMPLOYEE = "employee"

class Users(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20),nullable=False)

    tasks = relationship(
        'TaskManagger',
        back_populates="user",
        foreign_keys="TaskManagger.assigned_user",
        lazy='selectin',
        cascade='all,delete-orphan')

