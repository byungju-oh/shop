from app import create_app

app = create_app()
celery = app.celery

@celery.task
def register_user(username, phone_number, password):
    from app import db, bcrypt
    from app.models import User
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, phone_number=phone_number, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return {'status': 'success', 'message': 'User registered successfully'}
