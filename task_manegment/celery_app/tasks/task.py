

from celery_ import app  # Import Celery app instance
# from datetime import datetime
from Models.TaskLogger import TaskLogger, AuditLog
from Models.Task import TaskManagger
from extensions import db
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from extensions import create_app  # Ensure you import the Flask app factory
import datetime
# Create a Flask app instance
flask_app = create_app()


@app.task(bind=True,name='celery_app.tasks.task.transfer_active_tasks')
def transfer_active_tasks(self):
    try:

        # print("Daily transfer task is running at", datetime.now())

        # Get all active tasks
        with flask_app.app_context():

            active_tasks = db.session.query(TaskManagger).filter(TaskManagger.status == "TRUE").all()

            for task in active_tasks:
                # Check if already logged today
                existing_log = db.session.query(TaskLogger).filter(
                    TaskLogger.task_name == task.task_name,
                    # TaskLogger.logged_at == datetime.date.today()
                ).first()

                if not existing_log:
                    new_log = TaskLogger(task_name=task.task_name,
                                         description=task.description,
                                          
                                          status=task.status,
                                          priority=task.priority,
                                          assigned_user=task.assigned_user,
                                          logged_at=datetime.date.today()
                                          
                                          )
                    db.session.add(new_log)


            db.session.commit()
            print("celery logged success")
    except Exception as e:
        print(f" Task failed: {str(e)}")
        


















# from datetime import datetime
# from ...celery import celery
# from ..extensions import db

# @celery.task
# def transfer_active_tasks():
#     print(f"Task running at {datetime.now()}")
#     try:
#         # Your task logic here
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         raise e