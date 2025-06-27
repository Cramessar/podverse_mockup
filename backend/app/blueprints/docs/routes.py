from flask import render_template_string, send_file, Response
import os
from . import docs_bp 


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
      <style>
        .swagger-ui .scheme-container {
          background: #fafafa;
          padding: 20px;
          border-radius: 4px;
          margin-bottom: 20px;
        }
        .auth-btn-wrapper {
          display: flex;
          justify-content: flex-end;
          margin-bottom: 20px;
        }
        .authorize-btn {
          background: #741b47;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 4px;
          cursor: pointer;
          font-weight: bold;
        }
        .authorize-btn:hover {
          background: #5a1536;
        }
      </style>
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
          layout: "BaseLayout",
          deepLinking: true,
          showExtensions: true,
          showCommonExtensions: true,
          persistAuthorization: true,
          onComplete: function() {
            // Add custom instruction for Auth0 token
            const authContainer = document.querySelector('.scheme-container');
            if (authContainer && !document.querySelector('.auth-instructions')) {
              const instructions = document.createElement('div');
              instructions.className = 'auth-instructions';
              instructions.innerHTML = `
                <h4 style="margin-top: 0; color: #741b47;"> Authentication Instructions:</h4>
                <ol style="color: #333; line-height: 1.6;">
                  <li><strong>Get your Auth0 JWT token</strong> from your frontend login or Auth0 dashboard</li>
                  <li><strong>Go to Auth0 dashboard</strong> and click on Applications -> APIs -> Test tab to get your JWT token</li>
                  <li><strong>Click the "Authorize" button</strong> above</li>
                  <li><strong>Enter your JWT token</strong> in the "Value" field (without "Bearer " prefix)</li>
                  <li><strong>Click "Authorize"</strong> and then "Close"</li>
                  <li><strong>Test protected endpoints</strong> - they will now include your token automatically</li>
                </ol>
              `;
              authContainer.appendChild(instructions);
            }
          }
        });
      </script>
    </body>
    </html>
    """
    return render_template_string(swagger_html)
