#!/usr/bin/env python3

import re
import bs4
from bs4 import BeautifulSoup
import os
import shutil

def read_html_file(file_path):
    """Read the HTML file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_table_rows(html_content):
    """Extract all rows from the table in the HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    
    # Extract headers
    headers = []
    header_row = table.find('thead').find('tr')
    for th in header_row.find_all('th'):
        headers.append(th.text.strip())
    
    # Extract data rows
    rows = []
    tbody = table.find('tbody')
    for tr in tbody.find_all('tr'):
        row_data = []
        for td in tr.find_all('td'):
            row_data.append(td.text.strip())
        rows.append(row_data)
    
    return headers, rows

def generate_table_rows_html(rows):
    """Generate HTML for table rows from the extracted data."""
    html = ""
    for row in rows:
        html += "                <tr>\n"
        for cell in row:
            html += f"                    <td>{cell}</td>\n"
        html += "                </tr>\n"
    return html

def update_interactive_table(template_path, output_path, rows_html):
    """Update the interactive table template with the actual rows data."""
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    
    pattern = r'(<tbody>)(.*?)(</tbody>)'
    replacement = r'\1\n' + rows_html + r'            \3'
    
    updated_content = re.sub(pattern, replacement, template_content, flags=re.DOTALL)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def make_files_ready_for_publishing(js_file, html_file, output_dir):
    """Ensure files are in the right location for publishing."""
    os.makedirs(output_dir, exist_ok=True)
    shutil.copy2(js_file, os.path.join(output_dir, os.path.basename(js_file)))
    shutil.copy2(html_file, os.path.join(output_dir, os.path.basename(html_file)))
    print(f"Files copied to {output_dir}")

def main():
    original_table_path = 'notyet_interactive_table.html'
    template_path = 'interactive_table.html'
    js_path = 'interactive_table.js'
    output_path = 'interactive_table_full.html'
    publish_dir = '../../img'
    
    html_content = read_html_file(original_table_path)
    headers, rows = extract_table_rows(html_content)
    rows_html = generate_table_rows_html(rows)
    
    update_interactive_table(template_path, output_path, rows_html)
    
    make_files_ready_for_publishing(js_path, output_path, publish_dir)
    
    print(f"Interactive table created at {output_path}")
    print(f"Files also copied to {publish_dir} for easy inclusion in index.qmd")

if __name__ == "__main__":
    main() 