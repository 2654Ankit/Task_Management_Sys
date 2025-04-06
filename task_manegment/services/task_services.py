from repository.task_repository import TaskRepository
from flask import jsonify, make_response
import json, csv, io
from extensions import get_redis

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()
        self.redis = get_redis()

    def upload_csv(self, current_user, request):
        if current_user.role != "admin":
            return make_response({"message": "Unauthorized"}, 403)

        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            return make_response({"error": "Invalid file"}, 400)

        try:
            stream = io.StringIO(file.stream.read().decode("UTF8"))
            reader = csv.DictReader(stream)
            tasks = [row for row in reader]
            self.repo.bulk_insert_tasks(tasks)
            return make_response({"message": f"Uploaded {len(tasks)} tasks"}, 200)
        except Exception as e:
            return make_response({"error": str(e)}, 500)

    def create_task(self, current_user, data):
        if current_user.role != "admin":
            return make_response({"message": "Unauthorized"}, 403)

        self.repo.create_task(data)
        return make_response({"message": "Task created"}, 201)

    def modify_task(self, current_user, task_id, data):
        return self.repo.update_task(current_user, task_id, data)

    def update_status(self, current_user, task_id, data):
        return self.repo.soft_delete_task(current_user, task_id, data)

    def get_tasks(self, request):
        return self.repo.get_tasks_by_date(request)


