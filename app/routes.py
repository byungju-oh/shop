from flask import Blueprint, render_template, url_for, flash, redirect, request,current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Item ,Image
from app.forms import RegistrationForm, LoginForm, ImageForm
import os
import uuid
from prometheus_client import Summary
from google.cloud import storage
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="tete-426803-fcea6282bee1.json"
main = Blueprint('main', __name__)
users = Blueprint('users', __name__)
def extract_filename(url):
    filename = os.path.basename(url)
    name, ext = os.path.splitext(filename)
    # UUID 부분과 파일 이름 부분을 분리
    original_name = "_".join(name.split('_')[1:])
    return original_name

def upload_to_gcs(file, bucket_name):
    client = storage.Client()
    # client = storage.Client.from_service_account_json(current_app.config['GOOGLE_APPLICATION_CREDENTIALS'])
    bucket = client.bucket(bucket_name)
    # 원래 파일 이름을 사용하여 새로운 파일 이름 생성
    filename = file.filename
    new_filename = f"{uuid.uuid4()}_{filename}"
    blob = bucket.blob(f"images/{new_filename}")
    blob.upload_from_file(file)
    # 객체를 공개합니다.
    blob.make_public()
    return blob.public_url

def delete_from_gcs(url):
    client = storage.Client()
    # client = storage.Client.from_service_account_json(current_app.config['GOOGLE_APPLICATION_CREDENTIALS'])
    bucket_name = current_app.config['GCS_BUCKET_NAME']
    bucket = client.bucket(bucket_name)
    # URL에서 객체 이름 추출
    object_name = url.split(f"https://storage.googleapis.com/{bucket_name}/")[-1]
    blob = bucket.blob(object_name)
    blob.delete()

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


@main.route('/')
@main.route('/home')
@REQUEST_TIME.time()
def home():
    
    return render_template('index.html')

@main.route('/fashion')
@REQUEST_TIME.time()
def fashion():
    images = Image.query.all()
    images_with_filenames = [(image.id, image.url, extract_filename(image.url)) for image in images]
    return render_template('it.html', images=images_with_filenames)
    

@main.route('/electronic')
@REQUEST_TIME.time()
def electronic():
    images = Image.query.all()
    images_with_filenames = [(image.url, extract_filename(image.url)) for image in images]
    return render_template('infa.html', images=images_with_filenames)

@main.route('/jewellery')
@REQUEST_TIME.time()
def jewellery():
    return render_template('jewellery.html')

@users.route('/login', methods=['GET', 'POST'])
@REQUEST_TIME.time()
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@users.route('/register', methods=['GET', 'POST'])
@REQUEST_TIME.time()
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, phone_number=form.phone_number.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/logout')
@REQUEST_TIME.time()
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/cart')
@REQUEST_TIME.time()
@login_required
def cart():
    # cart = current_user.cart
    # if not cart:
    #     cart = Cart(user_id=current_user.id)
    #     db.session.add(cart)
    #     db.session.commit()
    return render_template('cart.html', cart=cart)

# @main.route('/add_to_cart/<int:item_id>', methods=['POST'])
# @login_required
# def add_to_cart(item_id):
#     item = Item.query.get_or_404(item_id)
#     cart = current_user.cart
#     if not cart:
#         cart = Cart(user_id=current_user.id)
#         db.session.add(cart)
#         db.session.commit()

#     cart_item = CartItem.query.filter_by(cart_id=cart.id, item_id=item.id).first()
#     if cart_item:
#         cart_item.quantity += 1
#     else:
#         cart_item = CartItem(cart_id=cart.id, item_id=item.id, quantity=1)
#         db.session.add(cart_item)
    
#     db.session.commit()
#     flash(f'Item {item.name} added to cart', 'success')
#     return redirect(url_for('main.home'))

@main.route('/search')
@REQUEST_TIME.time()
def search():
    query = request.args.get('query')
    items = Item.query.filter(Item.name.like(f'%{query}%')).all()
    return render_template('search_results.html', items=items, query=query)


# @users.route('/add_image', methods=['GET', 'POST'])
# @REQUEST_TIME.time()
# def add_image():
#     form = ImageForm()
#     if form.validate_on_submit():
#         new_image = Image(url=form.url.data)
#         db.session.add(new_image)
#         db.session.commit()
#         return redirect(url_for('main.home'))
#     return render_template('add_image.html', form=form)

@main.route('/add_image', methods=['GET', 'POST'])
@login_required
def add_image():
    form = ImageForm()
    if form.validate_on_submit():
        file = form.image.data
        url = upload_to_gcs(file, current_app.config['GCS_BUCKET_NAME'])
        new_image = Image(url=url)
        db.session.add(new_image)
        db.session.commit()
        flash('Image added successfully!', 'success')
        return redirect(url_for('main.fashion'))
    return render_template('adi.html', form=form)

@main.route('/delete_image/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    delete_from_gcs(image.url)
    db.session.delete(image)
    db.session.commit()
    flash('Image has been deleted!', 'success')
    return redirect(url_for('main.fashion'))