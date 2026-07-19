import os
import re

def split_engineering_editor():
    """
    Reads the single-file 'index.html', extracts CSS and JS,
    and creates a clean production-ready structure inside a 'dist' folder.
    """
    input_filename = 'index.html'
    output_dir = 'dist'
    
    # Check if the single file exists in the current directory
    if not os.path.exists(input_filename):
        print(f"Error: '{input_filename}' not found in the current folder.")
        print("Please save your TwaTemplato HTML file as 'index.html' in this directory and run the script again.")
        return

    print(f"Reading '{input_filename}'...")
    with open(input_filename, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Create output directory for separated production code
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: '{output_dir}/'")

    # Extract CSS content from <style>...</style> block
    css_pattern = re.compile(r'<style>(.*?)</style>', re.DOTALL)
    css_match = css_pattern.search(html_content)
    
    if css_match:
        css_content = css_match.group(1).strip()
        css_path = os.path.join(output_dir, 'style.css')
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("Successfully extracted styles -> 'dist/style.css'")
        
        # Replace the entire style tag with a link to external stylesheet
        html_content = css_pattern.sub('    <link rel="stylesheet" href="style.css">', html_content)
    else:
        print("Warning: No inline <style> block found to extract.")

    # Extract JS content from custom inline <script>...</script> block
    # This regex target scripts that do NOT have a 'src' attribute (which are external libraries like html2pdf)
    js_pattern = re.compile(r'<script(?![^>]*\bsrc\b)[^>]*>(.*?)</script>', re.DOTALL)
    js_match = js_pattern.search(html_content)

    if js_match:
        js_content = js_match.group(1).strip()
        js_path = os.path.join(output_dir, 'script.js')
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Successfully extracted interactive script -> 'dist/script.js'")
        
        # Replace inline script block with a source link to our new clean script.js file
        html_content = js_pattern.sub('    <script src="script.js"></script>', html_content)
    else:
        print("Warning: No inline custom <script> block found to extract.")

    # Write the newly cleaned HTML file
    clean_html_path = os.path.join(output_dir, 'index.html')
    with open(clean_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Successfully assembled clean structural template -> 'dist/index.html'")
    print("\nExtraction complete! Your clean backend assets are now ready inside the 'dist' directory.")

if __name__ == '__main__':
    split_engineering_editor()