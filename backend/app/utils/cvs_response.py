# app/utils/cvs_response.py

import csv
import io
from flask import Response, request, make_response, jsonify
from typing import List, Dict, Any
from app.utils.error_exceptions import ValidationError

def generate_csv_response(data: List[Dict[str, Any]], filename: str) -> Response:
    """
    Generate a CSV or JSON response from a list of dictionaries.

    Args:
        data: List of dictionaries representing rows
        filename: Name for the file download (extension will be appended automatically)

    Returns:
        Flask Response object with CSV or JSON content
    """
    format = request.args.get("format", "csv")
    if format not in ("csv", "json"):
        raise ValidationError("Unsupported format")

    # Ensure filename has correct extension
    if not filename.endswith(f'.{format}'):
        filename += f'.{format}'

    # Handle empty data
    if not data:
        if format == "json":
            return jsonify([])
        else:
            output = io.StringIO()
            output.write("")
            output.seek(0)
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )

    # Auto-generate headers from first row
    headers = {k: k for k in data[0].keys()}

    if format == "csv":
        output = io.StringIO()
        output.write('\ufeff')  # BOM for Excel
        writer = csv.DictWriter(output, fieldnames=headers.keys(), quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows({k: row.get(k, "") for k in headers} for row in data)
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-type"] = "text/csv"
        return response

    else:  # format == "json"
        return jsonify(data)
