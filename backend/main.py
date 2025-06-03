import os
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# Path to the OpenAPI YAML file
OPENAPI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "openapi.yaml")

@app.route("/openapi.yaml")
def openapi_yaml():
    with open(OPENAPI_PATH, "r") as f:
        yaml_content = f.read()
    return Response(yaml_content, mimetype="text/plain")

# Serve a simple Swagger UI page
@app.route("/docs")
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

# Simple homepage with links
@app.route("/")
def index():
    return """
    <h1>Podverse Admin API</h1>
    <ul>
      <li><a href="/docs">API Documentation (Swagger UI)</a></li>
      <li><a href="/openapi.yaml">OpenAPI Spec (YAML)</a></li>
      <li><a href="/admin">Admin API root (placeholder)</a></li>
    </ul>
    """

# Placeholder admin endpoint
@app.route("/admin")
def admin_root():
    return {"message": "Admin API is up and running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
