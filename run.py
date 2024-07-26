from app import create_app
from prometheus_client import start_http_server
from app import create_app
app = create_app()

if __name__ == '__main__':
    
    start_http_server(8000)
    app.run(debug=True)
