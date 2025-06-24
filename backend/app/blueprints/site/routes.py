from flask import Blueprint, current_app, render_template_string, url_for

site_bp = Blueprint("site", __name__)

@site_bp.route("/", strict_slashes=False)
def site_home():
    route_list = []

    for rule in current_app.url_map.iter_rules():
        # Filter only relevant /admin routes
        if (
            rule.rule.startswith("/admin")
            and "GET" in rule.methods
            and not rule.rule.startswith("/admin/site")
            and not rule.rule.endswith("/<path:filename>")
        ):
            route_list.append({
                "endpoint": rule.endpoint,
                "url": rule.rule
            })

    # Optional: Group routes by blueprint prefix
    # grouped = defaultdict(list)
    # for route in route_list:
    #     prefix = route["url"].split("/")[2] if len(route["url"].split("/")) > 2 else "root"
    #     grouped[prefix].append(route)

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Admin Sitemap</title>
        <style>
            body {
                background-color: #E5EAF2;
                font-family: 'Inter', sans-serif;
                color: #000000;
                padding: 2rem;
            }
            h1 {
                color: #741b47;
                font-size: 2rem;
                margin-bottom: 1rem;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                margin-bottom: 0.5rem;
                background: #ffffff;
                padding: 0.75rem 1rem;
                border-left: 4px solid #0D7AB3;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                transition: background 0.2s ease;
            }
            li:hover {
                background: #fae7b5;
            }
            a {
                color: #0D7AB3;
                text-decoration: none;
                font-weight: 600;
            }
            a:hover {
                text-decoration: underline;
            }
            .endpoint {
                color: #A0A0A0;
                font-size: 0.85rem;
            }
        </style>
    </head>
    <body>
        <h1>Admin Sitemap</h1>
        <ul>
          {% for route in routes %}
            <li>
              <a href="{{ route.url }}">{{ route.url }}</a><br>
              <span class="endpoint">(endpoint: {{ route.endpoint }})</span>
            </li>
          {% endfor %}
        </ul>
    </body>
    </html>
    """

    return render_template_string(html, routes=sorted(route_list, key=lambda r: r["url"]))
