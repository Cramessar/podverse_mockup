from flask import Blueprint, render_template_string, jsonify, Response
import os

docs_bp = Blueprint("docs", __name__)

OPENAPI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../openapi.yaml")

@docs_bp.route("/openapi.yaml")
def openapi_yaml():
    with open(OPENAPI_PATH, "r") as f:
        yaml_content = f.read()
    return Response(yaml_content, mimetype="text/plain")

@docs_bp.route("/docs")
def swagger_ui():
    swagger_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Podverse API Docs</title>
      <link href="https://unpkg.com/swagger-ui-dist@4/swagger-ui.css" rel="stylesheet" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
      <script>
        SwaggerUIBundle({
          url: "/openapi.yaml",
          dom_id: '#swagger-ui',
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
          ],
          layout: "BaseLayout"
        })
      </script>
    </body>
    </html>
    """
    return render_template_string(swagger_html)

@docs_bp.route("/")
def index():
    return jsonify({"status": "API running"})

@docs_bp.route("/admin")
def admin_root():
    return {"message": "Admin API is up and running"}
