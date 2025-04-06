from repository.logger_repository import LoggerRepository
from flask import make_response

class LoggerService:
    def __init__(self):
        self.repo = LoggerRepository()

    def get_task(self, task_logger_id):
        task = self.repo.get_task(task_logger_id)
        if not task:
            return make_response({"message": "Not found"}, 404)
        return make_response({"task": task})

