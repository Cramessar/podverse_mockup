# app/utils/cvs_response.py

import csv
import io
import xml.etree.ElementTree as ET
from datetime import datetime
from flask import Response, request, make_response, jsonify
from typing import List, Dict, Any
from app.utils.error_exceptions import ValidationError

def generate_export_response(data: List[Dict[str, Any]], filename: str, export_type: str = "feed") -> Response:
    """
    Generate a CSV, JSON, or OPML response from a list of dictionaries.

    Args:
        data: List of dictionaries representing rows
        filename: Name for the file download (extension will be appended automatically)
        export_type: Type of data being exported ('feed', 'channel', 'item', etc.) - affects OPML structure

    Returns:
        Flask Response object with CSV, JSON, or OPML content
    """
    format = request.args.get("format", "csv")
    if format not in ("csv", "json", "opml"):
        raise ValidationError("Unsupported format. Use 'csv', 'json', or 'opml'")
    
    # OPML is only supported for feeds
    if format == "opml" and export_type != "feed":
        raise ValidationError("OPML format is only supported for feeds. Use 'csv' or 'json' for other data types.")

    # Ensure filename has correct extension
    if not filename.endswith(f'.{format}'):
        filename += f'.{format}'

    # Handle empty data
    if not data:
        if format == "json":
            return jsonify([])
        elif format == "opml":
            return _generate_empty_opml_response(filename, export_type)
        else:  # csv
            output = io.StringIO()
            output.write("")
            output.seek(0)
            return Response(
                output.getvalue(),
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename="{filename}"'}
            )

    # Auto-generate headers from first row for CSV
    headers = {k: k for k in data[0].keys()}

    if format == "csv":
        return _generate_csv_response(data, headers, filename)
    elif format == "json":
        return jsonify(data)
    else:  # format == "opml"
        return _generate_opml_response(data, filename, export_type)

def _generate_csv_response(data: List[Dict[str, Any]], headers: Dict[str, str], filename: str) -> Response:
    """Generate CSV response"""
    output = io.StringIO()
    output.write('\ufeff')  # BOM for Excel
    writer = csv.DictWriter(output, fieldnames=headers.keys(), quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows({k: row.get(k, "") for k in headers} for row in data)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-type"] = "text/csv"
    return response

def _generate_opml_response(data: List[Dict[str, Any]], filename: str, export_type: str) -> Response:
    """Generate OPML response (primarily for feeds/podcasts)"""
    # Create OPML structure
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    
    # Add head metadata
    ET.SubElement(head, "title").text = f"Podverse {export_type.title()} Export"
    ET.SubElement(head, "dateCreated").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
    ET.SubElement(head, "docs").text = "http://dev.opml.org/spec2.html"
    
    body = ET.SubElement(opml, "body")
    
    # Add data as outline elements
    for item in data:
        outline_attrs = _map_data_to_opml_attributes(item, export_type)
        ET.SubElement(body, "outline", outline_attrs)
    
    # Convert to string
    ET.indent(opml, space="  ")
    xml_string = ET.tostring(opml, encoding="unicode", xml_declaration=True)
    
    response = make_response(xml_string)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response

def _generate_empty_opml_response(filename: str, export_type: str) -> Response:
    """Generate empty OPML structure"""
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    ET.SubElement(head, "title").text = f"Podverse {export_type.title()} Export"
    ET.SubElement(head, "dateCreated").text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")
    ET.SubElement(opml, "body")
    
    xml_string = ET.tostring(opml, encoding="unicode", xml_declaration=True)
    response = make_response(xml_string)
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response

def _map_data_to_opml_attributes(item: Dict[str, Any], export_type: str) -> Dict[str, str]:
    """Map data fields to OPML outline attributes based on export type"""
    attrs = {}
    
    if export_type == "feed":
        # Standard OPML 2.0 attributes for RSS feeds
        attrs["type"] = "rss"
        attrs["text"] = str(item.get("title", "Untitled"))
        attrs["title"] = str(item.get("title", "Untitled"))
        attrs["xmlUrl"] = str(item.get("url", ""))
        
        # Optional attributes
        if item.get("description"):
            attrs["description"] = str(item["description"])
        if item.get("website_url"):
            attrs["htmlUrl"] = str(item["website_url"])
        if item.get("category"):
            attrs["category"] = str(item["category"])
            
    elif export_type == "channel":
        # Adapt channel data to OPML format
        attrs["text"] = str(item.get("title", "Untitled Channel"))
        attrs["title"] = str(item.get("title", "Untitled Channel"))
        if item.get("feed_url"):
            attrs["type"] = "rss"
            attrs["xmlUrl"] = str(item["feed_url"])
        if item.get("website_url"):
            attrs["htmlUrl"] = str(item["website_url"])
            
    else:
        # Generic mapping for other types
        attrs["text"] = str(item.get("title") or item.get("name") or "Untitled")
        if "url" in item:
            attrs["url"] = str(item["url"])
    
    # Clean empty attributes
    return {k: v for k, v in attrs.items() if v}

# Backward compatibility
def generate_csv_response(data: List[Dict[str, Any]], filename: str) -> Response:
    """
    Backward compatibility function - use generate_export_response instead
    """
    return generate_export_response(data, filename, "generic")
