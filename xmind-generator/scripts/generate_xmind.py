#!/usr/bin/env python3
"""
Generate XMind mind map files from structured data.

Usage:
    python generate_xmind.py <output_file> <data_json>
    
Example:
    python generate_xmind.py output.xmind '{"root":"Project","children":[...]}'
"""

import json
import sys
import zipfile
import os
from pathlib import Path
from xml.dom import minidom


def create_xmind_content(data, root_title="Mindmap"):
    """Create the content.xml for XMind file."""
    
    # XMind content.xml template with basic structure
    xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
    
    def build_topic_xml(topic_data, level=1):
        """Recursively build topic XML."""
        if isinstance(topic_data, str):
            title = topic_data
            children = []
        elif isinstance(topic_data, dict):
            title = topic_data.get("title") or topic_data.get("name", "")
            children = topic_data.get("children", [])
        else:
            return ""
        
        # Escape XML special characters
        title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        
        children_xml = ""
        if children:
            for child in children:
                children_xml += build_topic_xml(child, level + 1)
        
        child_elem = f"<children>{children_xml}</children>" if children_xml else ""
        
        return f'''<topic id="topic_{level}_{hash(title) % 10000}" structureClass="org.xmind.ui.logic.left">
            <title>{title}</title>
            {child_elem}
        </topic>'''
    
    # Build root topic
    root_title = root_title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    root_xml = build_topic_xml(data, level=0)
    
    if not root_xml:
        # Fallback if data is empty
        root_xml = f'<topic id="root"><title>{root_title}</title></topic>'
    
    content_xml = f'''{xml_header}
<xmap-content xmlns="urn:xmind:xmap:xmlns:content:2.0" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:svg="http://www.w3.org/2000/svg">
    <sheet id="sheet1" version="2.0">
        <title>{root_title}</title>
        <rootTopic id="root">
            <title>{root_title}</title>
            <children type="attached">
                {root_xml}
            </children>
        </rootTopic>
        <relationships/>
    </sheet>
</xmap-content>'''
    
    return content_xml


def create_metadata_xml():
    """Create metadata.xml for XMind."""
    metadata_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="urn:xmind:metadata:xmlns:1.0" Version="2.0"></metadata>'''
    return metadata_xml


def create_styles_xml():
    """Create styles.xml for XMind."""
    styles_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<xmap-styles xmlns="urn:xmind:xmap:xmlns:style:2.0" xmlns:svg="http://www.w3.org/2000/svg" xmlns:fo="http://www.w3.org/1999/XSL/Format">
    <style id="default" name="default"/>
</xmap-styles>'''
    return styles_xml


def create_manifest_xml():
    """Create manifest.xml for XMind."""
    manifest_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns="urn:xmind:xmap:xmlns:manifest:2.0">
    <file-entry full-path="content.xml" media-type="text/xml"/>
    <file-entry full-path="metadata.xml" media-type="text/xml"/>
    <file-entry full-path="styles.xml" media-type="text/xml"/>
    <file-entry full-path="/" media-type="application/vnd.xmind.workbook"/>
</manifest>'''
    return manifest_xml


def generate_xmind_file(output_path, data, root_title="Mindmap"):
    """Generate a complete XMind file."""
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a temporary zip file (XMind is just a ZIP)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as xmind_zip:
        # Add content.xml
        content = create_xmind_content(data, root_title)
        xmind_zip.writestr('content.xml', content.encode('utf-8'))
        
        # Add metadata.xml
        metadata = create_metadata_xml()
        xmind_zip.writestr('metadata.xml', metadata.encode('utf-8'))
        
        # Add styles.xml
        styles = create_styles_xml()
        xmind_zip.writestr('styles.xml', styles.encode('utf-8'))
        
        # Add manifest.xml
        manifest = create_manifest_xml()
        xmind_zip.writestr('META-INF/manifest.xml', manifest.encode('utf-8'))
    
    return str(output_path)


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_xmind.py <output_file> <json_data_or_file> [root_title]")
        print("\nExample with inline JSON:")
        print('  python generate_xmind.py output.xmind \'{"title":"Root","children":[{"title":"Node1"},{"title":"Node2"}]}\'')
        print("\nExample with JSON file:")
        print('  python generate_xmind.py output.xmind data.json "My Mindmap"')
        sys.exit(1)
    
    output_file = sys.argv[1]
    data_input = sys.argv[2]
    root_title = sys.argv[3] if len(sys.argv) > 3 else "Mindmap"
    
    # Try to parse as JSON
    try:
        if os.path.isfile(data_input):
            with open(data_input, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = json.loads(data_input)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found - {data_input}")
        sys.exit(1)
    
    # Generate XMind file
    try:
        result = generate_xmind_file(output_file, data, root_title)
        print("XMind file created: " + result)
        return 0
    except Exception as e:
        print("Error: Failed to create XMind file - " + str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
