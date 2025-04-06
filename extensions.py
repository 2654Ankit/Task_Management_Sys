import os
from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import redis
from tenacity import retry, stop_after_attempt, wait_fixed
from sqlalchemy.exc import OperationalError

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Retry config for DB
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def try_database_connection(uri):
    try:
        engine = db.create_engine(uri)
        with engine.connect() as conn:
            pass  # Test connection
    except OperationalError as e:
        print(" Failed to connect to DB. Retrying...")
        raise e

def create_app():
    app = Flask(__name__)
    
    db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Test DB connection with retry
    try_database_connection(db_uri)

    # Configure SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    return app

# Retry config for Redis
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def get_redis():
    try:
        pool = redis.ConnectionPool(
            host=os.getenv('REDIS_HOST', 'localhost'),
            port=int(os.getenv('REDIS_PORT', 6379)),
            db=int(os.getenv('REDIS_DB', 0)),
            decode_responses=True
        )
        rds = redis.Redis(connection_pool=pool)
        
        return rds
    except redis.exceptions.ConnectionError as e:
        print("  Failed to connect to Redis. Retrying...")
        raise e
