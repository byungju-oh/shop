import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import make_wsgi_app, Gauge, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask_redis import FlaskRedis
from celery import Celery

load_dotenv()  # Load .env file

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

IN_PROGRESS = Gauge('inprogress_requests', 'Number of requests in progress')
REQUEST_COUNTER = Counter('http_requests_total', 'Total number of HTTP requests')

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['GCS_BUCKET_NAME'] = os.getenv('GCS_BUCKET_NAME')
    app.config['REDIS_URL'] = "redis://redis:6379/0"
    app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
    
    metrics = PrometheusMetrics(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    redis_client = FlaskRedis(app)
    celery = make_celery(app)
    
    app.celery = celery  # Add celery instance to app
    
    from app.routes import main, users
    app.register_blueprint(main)
    app.register_blueprint(users)
    
    # Add Prometheus WSGI middleware to route /metrics requests
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    
    @app.before_request
    def before_request():
        IN_PROGRESS.inc()  # Increment the gauge
        REQUEST_COUNTER.inc()  # Increment the counter

    @app.after_request
    def after_request(response):
        IN_PROGRESS.dec()  # Decrement the gauge
        return response

    # Google Cloud Credentials
    google_credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if google_credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
    
    with app.app_context():
        retries = 5
        while retries > 0:
            try:
                inspector = inspect(db.engine)
                if not inspector.has_table('user') or not inspector.has_table('item') or not inspector.has_table('cart') or not inspector.has_table('cartitem'):
                    db.create_all()
                break
            except OperationalError as e:
                retries -= 1
                print(f"DB connection failed. Retrying... ({5 - retries}/5)")
                time.sleep(5)
                if retries == 0:
                    print("DB connection failed after 5 retries.")
                    raise e
    return app
