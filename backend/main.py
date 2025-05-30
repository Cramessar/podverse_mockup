from flask import Flask
from flasgger import Swagger
from routes.routes import routes_bp

app = Flask(__name__)
swagger = Swagger(app)

app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug=True)
