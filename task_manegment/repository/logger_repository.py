from Models.TaskLogger import TaskLogger

class LoggerRepository:
    def get_task(self, task_logger_id):
        task = TaskLogger.query.filter_by(id=task_logger_id).first()
        if task:
            return {
                "id": task.id,
                "task_name": task.task_name,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "assigned_user": task.assigned_user,
                "logged_at": str(task.logged_at)
            }
        return None
