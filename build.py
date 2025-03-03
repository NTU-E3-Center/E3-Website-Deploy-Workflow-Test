import os
import shutil
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

# Load pages from an external JSON file
with open("contents/pages.json", "r") as f:
    pages = json.load(f)

# Loop through each file in the folder
contents_path = 'contents'
contents = {}
for filename in os.listdir(contents_path):
    if filename.endswith('.json'):
        file_path = os.path.join(contents_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            # Load JSON content
            data = json.load(f)
        # Create a key based on the file name (without the .json extension)
        var_name = os.path.splitext(filename)[0]
        contents[var_name] = data

# Output directory
output_dir = "dist"

# Function to render templates into correct directories
def render_templates():
    def process_pages(pages, base_path=""):
        for template_name, page_data in pages.items():
            if isinstance(page_data, dict) and "path" in page_data:
                template = env.get_template(f"{template_name}.html")
                output = template.render(
                    title=page_data.get("title"),
                    updated_time=datetime.now().strftime("%Y. %m. %d"),
                    contents=contents
                )
                
                # Define full output path (subdirectories)
                page_dir = os.path.join(output_dir, base_path, page_data["path"])
                os.makedirs(page_dir, exist_ok=True)
                
                # Save the rendered HTML inside index.html
                with open(os.path.join(page_dir, "index.html"), "w", encoding="utf-8") as f:
                    f.write(output)
            elif isinstance(page_data, dict):  # If it's a nested structure without "path"
                process_pages(page_data, os.path.join(base_path, template_name))
    
    process_pages(pages)
    print("Templates rendered successfully!")

# Function to copy static assets directly into dist/
def copy_static():
    static_src = "static"
    if os.path.exists(static_src):
        for item in os.listdir(static_src):
            src_path = os.path.join(static_src, item)
            dst_path = os.path.join(output_dir, item)
            
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)

    print("Static assets copied directly into dist/")

# Run the build process
if __name__ == "__main__":
    print("Building static site...")
    render_templates()
    copy_static()
    print("Build complete!")
