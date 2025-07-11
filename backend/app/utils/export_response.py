# app/utils/export_response.py

import csv
import io
from flask import Response, request, make_response, jsonify
from typing import List, Dict, Any
from app.utils.error_exceptions import ValidationError

def generate_export_response(data: List[Dict[str, Any]], filename: str) -> Response:
    """
    Generate a CSV or JSON response from a list of dictionaries. 
    Default is CSV

    Args:
        data: List of dictionaries representing rows
        filename: Base filename (extension added automatically)

    Returns:
        Flask Response with content
    """
    format = request.args.get("format", "csv").lower()
    if format not in ("csv", "json"):
        raise ValidationError("Unsupported format. Use 'csv', 'json', or 'opml'")

    # Ensure filename has correct extension
    if not filename.endswith(f'.{format}'):
        filename += f'.{format}'

    # Handle empty data
    if not data:
        return jsonify([]) if format == "json" else generate_empty_csv_response(filename)

    if format == "json":
        return jsonify(data)
    else:
        headers = {k: k for k in data[0].keys()}
        return generate_csv_response(data, headers, filename)

def generate_csv_response(data: List[Dict[str, Any]], headers: Dict[str, str], filename: str) -> Response:
    output = io.StringIO()
    output.write('\ufeff')  # BOM for Excel
    writer = csv.DictWriter(output, fieldnames=headers.keys(), quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows({k: row.get(k, "") for k in headers} for row in data)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "text/csv"
    return response

def generate_empty_csv_response(filename: str) -> Response:
    output = io.StringIO()
    output.write("")
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response