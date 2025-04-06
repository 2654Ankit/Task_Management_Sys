from extensions import db
from sqlalchemy.sql import func
from datetime import datetime

class TaskLogger(db.Model):
    __tablename__ = 'TaskLogger'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255))
    description = db.Column(db.Text)
    status = db.Column(db.String(50))
    priority = db.Column(db.String(50))
    assigned_user = db.Column(db.String(255))
    logged_at = db.Column(db.Date, default=datetime.utcnow)


class AuditLog(db.Model):
    __tablename__ = 'audit_log'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    previous_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50))
    changed_by = db.Column(db.String(255))  # username
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
