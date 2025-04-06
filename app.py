from Models.User import Users
from flask import request,make_response,jsonify
from Models.Task import TaskManagger
from Models.TaskLogger import TaskLogger,AuditLog
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from functools import wraps
import json
from datetime import datetime,timedelta,timezone
from Models.TaskLogger import TaskLogger,AuditLog
from datetime import datetime
from extensions import db,get_redis,create_app
app = create_app()
redis_client = get_redis()
import csv
import io
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

with app.app_context():
    db.create_all()  


limiter = Limiter(key_func=get_remote_address,app=app,storage_uri=os.getenv("RATE_LIMIT_STORAGE_URI"))
#  This is the signup route. 
@app.route('/signup',methods=["POST"])
@limiter.limit("10 per minute")

def signup():
    data = request.json
    username = data.get("username")
    pas = data.get("password")
    print(pas)
    role = data.get("role")

    if username and pas and role:
        user=Users.query.filter_by(username=username).first()
        if user:
            return make_response(
                {"message":"Please sign in"},
                200
            )
        
        

        user = Users(
            username=username,
            password=generate_password_hash(pas),
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return make_response(
            {"message":"user created"},
            201
        )
    return make_response(
        {"message":"User not created"},
        500
    )



# Login route

@app.route("/login",methods=["POST"])
@limiter.limit("10 per minute")

def login():
    auth= request.json

    if not auth or not auth.get("username") or not auth.get("password"):
        return make_response(
            "Proper Credentials not provided",
            401

        )
    user = Users.query.filter_by(username=auth.get("username")).first()

    if not user:
        return make_response(
            "please create an account",
            401
        )
    if check_password_hash(user.password,auth.get('password')):
        token = jwt.encode({
            'username':user.username,
            'exp':datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        "secret",
        "HS256"
        )

        return make_response({"token":token})
    return make_response(
        'Please check your credintials',
        401
    )

# custom token_required code
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"]
            print(token)
        if not token:
            return make_response({"message":"token is missing"})
        
        try:
            data = jwt.decode(token,"secret",algorithms=["HS256"])
            current_user = Users.query.filter_by(username=data["username"]).first()

            print(current_user)

        except Exception as e:
            print(e)
            return make_response({"message":"Token is invalid"},
            401)

        return f(current_user,*args,**kwargs)

    return decorated


# Load  csv_file into TaskManager Table. 
@app.route('/upload-csv', methods=["POST"])   # done
@token_required
@limiter.limit("10 per minute")
def upload_csv(curr_user):
    print(curr_user.role)
    if  curr_user.role=="admin":

        if 'file' not in request.files:
            return make_response(jsonify({"error": "No file part in the request"}), 400)

        file = request.files['file']

        if file.filename == '':
            return make_response(jsonify({"error": "No selected file"}), 400)

        if not file.filename.endswith('.csv'):
            return make_response(jsonify({"error": "Invalid file format. Upload a CSV file."}), 400)

        try:
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)

            tasks_to_add = []
            for row in reader:
                task = TaskManagger(
                    task_name=row.get('task_name'),
                    description=row.get('description'),
                    priority=row.get('priority'),
                    assigned_user=row.get('assigned_user'),
                    status=row.get('status'),
                    created_at=row.get('created_at')
                )
                tasks_to_add.append(task)

            db.session.bulk_save_objects(tasks_to_add)
            db.session.commit()

            return make_response(jsonify({"message": f"Successfully uploaded {len(tasks_to_add)} tasks."}), 200)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": f"Upload failed: {str(e)} first register all users"}), 500)

    else:
        return make_response({"message":"you are not eligible to upload file"})
    


# Paginated list of all tasks from TaskLogger
def tasks():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    print(page,per_page)

    pagination = TaskLogger.query.paginate(page=page, per_page=per_page, error_out=False)
    
    tasks = [
        {
            "id": task.id,
            "task_name": task.task_name,
            "logged_at": task.logged_at.strftime("%Y-%m-%d") if task.logged_at else None
        }
        for task in pagination.items
    ]

    return jsonify({
        "tasks": tasks,
        "total": pagination.total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": pagination.pages
    })




# List tasks filtered by date with caching (Redis). 
@app.route("/tasks",methods=["GET"]) 
@limiter.limit("10 per minute")
def get_tasks():
    try:
        date = request.args.get("date")
        if not date:
            return make_response(tasks())

        if not date:
            return make_response({"error": "date is required"}, 400)

        cache_key = f"date:{date}"
        val = redis_client.get(cache_key)

        if val:
            task = json.loads(val)
            print("Redis cache hit")
            return make_response(jsonify(task), 200)

        # Query database if not found in Redis
        task = TaskManagger.query.filter_by(created_at=date).all()
        response = {}

        if task:
            response["tasks"] = [
                {
                    "task_name": t.task_name,
                    "description": t.description,
                    "status": t.status,
                    "priority": t.priority,
                    "assigned_user": t.assigned_user,
                    "created_at": str(t.created_at)  # Ensure date is JSON serializable
                }
                for t in task
            ]
        else:
            response = {"message": "No tasks found for this date"}

        # Only cache if tasks exist
        if "tasks" in response:
            redis_client.setex(cache_key, 3600, json.dumps(response))  # Cache for 1 hour
            print("Stored in Redis")

        print("hello")  # Just a debug print
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        return make_response(jsonify({"error":str(e)}))

# Retrieve task details, ensuring minimal DB queries. 
@app.route("/task/<task_logger_id>")
@token_required
@limiter.limit("10 per minute")
def get_task_from_tasklogger(curr_user,task_logger_id):
    try:
        t = TaskLogger.query.filter_by(id=task_logger_id).first()

        if not t :
            return make_response({"message":f"task with {task_logger_id} is not available in tasklogger"})
        
            
        res =    {
                "id":t.id,
                "task_name": t.task_name,
                "description": t.description,
                "status": t.status,
                "priority": t.priority,
                "assigned_user": t.assigned_user,
                "logged_at": t.logged_at  # Ensure date is JSON serializable
            }
        
        return make_response({"task":res})
    
    except Exception as e:
        return make_response({"error":jsonify(str(e))})




# Create a task, requiring JWT-based authentication.
@app.route("/create_task",methods=["POST"])
@token_required
@limiter.limit("10 per minute")
def create_task(curr_user):
    print(curr_user)

    if curr_user.role=="admin":
        data = request.json
        id = data.get("id")
        task_name = data.get("task_name")
        description = data.get("description")
        status = data.get("status")
        priority = data.get("priority")
        assigned_user = data.get("assigned_user")
        created_at = data.get("date")

        if task_name and description and status and priority and assigned_user:
            task = TaskManagger(
                task_name=task_name,
                description=description,
                status=status,
                priority=priority,
                assigned_user=assigned_user,
                created_at = created_at
            )
            db.session.add(task)
            db.session.commit()

            return make_response(
                {"message":"task assigned"},
                201
            )
        
        return make_response({"message":"All fields are not given"})

    return make_response({"message":"You are not authorized for creating task"})



# Updatinf a task status
@app.route("/task/<task_id>",methods=["PUT"])
@token_required
@limiter.limit("10 per minute")
def modify_task(curr_user,task_id):
    if curr_user.role == "admin":
        try:
            data = request.json

            if not data:
                return make_response({"message":"no update value provided"})
            
            task = TaskManagger.query.filter_by(task_id=task_id).first()
            if not task:
                return make_response({"message":f"the task with id {task_id} is not available"})
            
            prev_status = task.status
            
            for key in data.keys():
                setattr(task,key,data.get(key))

       
            
            if 'status' in data.keys():
                audit = AuditLog(
                    task_id=task.task_id, previous_status=prev_status,
                    new_status=data.get("status"),
                    changed_by=curr_user.username
                    )
                db.session.add(audit)
            db.session.commit()
            
            return make_response({"message":"task is updated"})
        except Exception  as e:
            return make_response({'error':str(e)})

    else:
        return make_response({"message":"you are not authorized for updating  task"})



# Soft delete a task (mark as inactive/FALSE). 
@app.route("/task/<task_id>",methods=["DELETE"])
@token_required
@limiter.limit("10 per minute")
def update_status(curr_user,task_id):
    try:
        task = TaskManagger.query.filter_by(task_id=task_id).first()

        if not task:
            return make_response({"messgae":f"Task with id {task_id} id not available"})
        
        if task.assigned_user != curr_user.username:
            return make_response({"message":"You are not permitted to inactive this task"})
        data = request.json
        if not data.get("status"):
            return make_response({"messgae":"please provide status fieLd"})
        
        task.status = data.get("status")

        db.session.commit()
        return make_response({"message":f"Task is marked as {data.get('status')}"})

    except Exception as e:
        return make_response(jsonify({"error":str(e)}))



@app.route("/delete_task/<task_id>",methods=["DELETE"])
@token_required
@limiter.limit("10 per minute")
def delete_task(curr_user,task_id):
    if curr_user.role == 'admin':
        task = TaskManagger.query.filter_by(task_id =task_id).first()
        if not task:
            return make_response({"message":f'task with {task_id} do not exist'})
        db.session.delete(task)
        db.session.commit()
        return make_response({'message':'task is deleted'})

    else:
        return make_response({"message":"You are not autorized to remove task"})







if __name__=="__main__":
    app.run(debug=True)