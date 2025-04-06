from extensions import db
from sqlalchemy.sql import func
# from Models.User import Users
from sqlalchemy.orm import relationship,backref










class TaskManagger(db.Model):
    __tablename__="TaskManagger"
    task_id = db.Column(db.Integer,primary_key=True)
    task_name = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(100),nullable=False)

    status = db.Column(db.String(100),nullable=False)

    priority = db.Column(db.String(100),nullable=False)
    assigned_user = db.Column(db.String(100),db.ForeignKey("Users.username"),nullable=False)
    user = relationship("Users", back_populates="tasks", lazy="joined")
    created_at = db.Column(db.Date,nullable=False)
    user = db.relationship(
        "Users",
        back_populates="tasks",
        foreign_keys=[assigned_user],
        lazy="joined"
    )
    # taskMgr = db.relationship('Users',backref="TaskManagger")