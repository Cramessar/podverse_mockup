from flask import render_template_string, send_file, Response
import os
from app.blueprints import docs_bp

OPENAPI_BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "openapi")
)
BUNDLED_PATH = os.path.join(OPENAPI_BASE, "bundled.yaml")

@docs_bp.route("/openapi.yaml")
def openapi_yaml():
    # Serve the bundled OpenAPI spec as text/yaml
    with open(BUNDLED_PATH, "r") as f:
        yaml_content = f.read()
    return Response(yaml_content, mimetype="text/yaml")

@docs_bp.route("/")
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
          url: "/admin/docs/openapi.yaml",
          dom_id: '#swagger-ui',
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
          ],
          layout: "BaseLayout"
        });
      </script>
    </body>
    </html>
    """
    return render_template_string(swagger_html)
