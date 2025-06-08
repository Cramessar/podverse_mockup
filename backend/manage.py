from app import create_app
from app.extensions import db

app = create_app('DevelopmentConfig')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)