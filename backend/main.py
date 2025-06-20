from app import create_app
from app.extensions import db
from dotenv import load_dotenv
import os

load_dotenv() # loads .env from root

config_name = os.getenv("FLASK_ENV", "development")
app = create_app(config_name)

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True, host="0.0.0.0", port=8000, use_reloader=False)
    except Exception as e:
        print("Fatal error during startup:", e)
