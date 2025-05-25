# Flask E-commerce Shop 🛒

A modern e-commerce web application built with Flask, featuring user authentication, product management, image upload to Google Cloud Storage, and real-time monitoring with Prometheus.

## 🌟 Features

- **User Authentication**: Registration, login, and logout functionality
- **Product Categories**: Fashion, Electronics, and Jewellery sections
- **Image Management**: Upload and delete product images with Google Cloud Storage integration
- **Shopping Cart**: Add items to cart (user authentication required)
- **Async Processing**: Celery integration for background tasks like user registration
- **Monitoring**: Prometheus metrics for application performance tracking
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **Multi-language Support**: English and Korean interface elements

## 🏗️ Architecture

```
├── app/
│   ├── __init__.py          # Application factory and configuration
│   ├── models.py            # Database models (User, Item, Cart, Image)
│   ├── routes.py            # Application routes and view functions
│   ├── forms.py             # WTForms for user input validation
│   ├── tasks.py             # Celery background tasks
│   ├── celery.py            # Celery configuration
│   └── templates/           # Jinja2 HTML templates
├── requirements.txt         # Python dependencies
├── run.py                  # Application entry point
├── Dockerfile              # Container configuration
└── .env                    # Environment variables
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- MySQL database
- Redis server (for Celery)
- Google Cloud Storage account (for image uploads)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-ecommerce-shop
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URI=mysql+pymysql://username:password@host/database
   SECRET_KEY=your-secret-key-here
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json
   GCS_BUCKET_NAME=your-bucket-name
   ```

4. **Set up Google Cloud Storage**
   - Create a GCS bucket
   - Download service account credentials
   - Update the path in your `.env` file

5. **Start Redis server**
   ```bash
   redis-server
   ```

6. **Start Celery worker**
   ```bash
   celery -A app.celery worker --loglevel=info
   ```

7. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`
Prometheus metrics at `http://localhost:8000`

## 🐳 Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t flask-shop .
   ```

2. **Run with Docker Compose** (recommended)
   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - "5000:5000"
       environment:
         - DATABASE_URI=mysql+pymysql://user:pass@db/shopdb
         - SECRET_KEY=your-secret-key
       depends_on:
         - db
         - redis
     
     db:
       image: mysql:8.0
       environment:
         - MYSQL_ROOT_PASSWORD=rootpass
         - MYSQL_DATABASE=shopdb
         - MYSQL_USER=user
         - MYSQL_PASSWORD=pass
     
     redis:
       image: redis:alpine
     
     celery:
       build: .
       command: celery -A app.celery worker --loglevel=info
       depends_on:
         - redis
         - db
   ```

## 📊 API Endpoints

### Authentication
- `GET /register` - User registration form
- `POST /register` - Process registration
- `GET /login` - Login form
- `POST /login` - Process login
- `GET /logout` - User logout

### Product Management
- `GET /` - Homepage with featured products
- `GET /fashion` - Fashion products with image management
- `GET /electronic` - Electronics products
- `GET /jewellery` - Jewellery products
- `GET /search` - Product search

### Image Management
- `GET /add_image` - Image upload form (auth required)
- `POST /add_image` - Upload image to GCS (auth required)
- `POST /delete_image/<id>` - Delete image (auth required)

### Shopping
- `GET /cart` - View shopping cart (auth required)

## 🛠️ Technologies Used

- **Backend**: Flask 2.0.2, SQLAlchemy, Flask-Login
- **Database**: MySQL with PyMySQL connector
- **Task Queue**: Celery with Redis broker
- **Cloud Storage**: Google Cloud Storage
- **Monitoring**: Prometheus with custom metrics
- **Frontend**: Bootstrap 4, jQuery, Font Awesome
- **Forms**: Flask-WTF for CSRF protection and validation
- **Security**: Bcrypt for password hashing

## 📈 Monitoring

The application includes Prometheus metrics for:
- Request processing time
- Number of requests in progress
- Total HTTP request counter

Access metrics at `http://localhost:8000/metrics`

## 🔧 Configuration

Key configuration options in `app/__init__.py`:

```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['GCS_BUCKET_NAME'] = os.getenv('GCS_BUCKET_NAME')
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'
```

## 🗄️ Database Schema

### User Model
- `id`: Primary key
- `username`: Unique username
- `phone_number`: Contact number
- `password`: Bcrypt hashed password
- `image_file`: Profile image (default: 'default.jpg')

### Image Model
- `id`: Primary key
- `url`: Google Cloud Storage URL

### Item Model
- `id`: Primary key
- `name`: Product name
- `price`: Product price
- `description`: Product description
- `image_file`: Product image
- `user_id`: Foreign key to User

### Cart & CartItem Models
- Shopping cart functionality with quantity tracking

## 🚦 Development

### Running in Development Mode
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python run.py
```

### Testing
```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## 🔮 Future Enhancements

- [ ] Payment gateway integration
- [ ] Order management system
- [ ] Product reviews and ratings
- [ ] Inventory management
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Advanced search and filters
- [ ] Wishlist functionality
- [ ] Multi-vendor support

---

**Made with ❤️ using Flask and modern web technologies**
