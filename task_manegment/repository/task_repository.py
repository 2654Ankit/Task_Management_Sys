from Models.Task import TaskManagger
from Models.TaskLogger import AuditLog
from extensions import db
from flask import jsonify, make_response
import json

class TaskRepository:
    def bulk_insert_tasks(self, tasks):
        objects = [TaskManagger(**task) for task in tasks]
        db.session.bulk_save_objects(objects)
        db.session.commit()

    def create_task(self, data):
        task = TaskManagger(**data)
        db.session.add(task)
        db.session.commit()

    def update_task(self, user, task_id, data):
        if user.role != "admin":
            return make_response({"message": "Unauthorized"}, 403)

        task = TaskManagger.query.filter_by(task_id=task_id).first()
        if not task:
            return make_response({"message": "Task not found"}, 404)

        prev_status = task.status
        for key, value in data.items():
            setattr(task, key, value)

        if 'status' in data:
            audit = AuditLog(task_id=task.task_id, previous_status=prev_status, new_status=data['status'], changed_by=user.username)
            db.session.add(audit)

        db.session.commit()
        return make_response({"message": "Task updated"}, 200)

    def soft_delete_task(self, user, task_id, data):
        task = TaskManagger.query.filter_by(task_id=task_id).first()
        if not task:
            return make_response({"message": "Task not found"}, 404)

        if task.assigned_user != user.username:
            return make_response({"message": "Unauthorized"}, 403)

        task.status = data.get("status")
        db.session.commit()
        return make_response({"message": f"Task marked as {task.status}"}, 200)

    def get_tasks_by_date(self, request):
        from extensions import get_redis
        redis_client = get_redis()

        date = request.args.get("date")
        if not date:
            return make_response(jsonify({"error": "date is required"}), 400)

        cache_key = f"date:{date}"
        cached = redis_client.get(cache_key)

        if cached:
            return make_response(jsonify(json.loads(cached)), 200)

        tasks = TaskManagger.query.filter_by(created_at=date).all()
        if tasks:
            response = {"tasks": [t.serialize() for t in tasks]}
            redis_client.setex(cache_key, 3600, json.dumps(response))
            return make_response(jsonify(response), 200)
        return make_response(jsonify({"message": "No tasks found"}), 200)

