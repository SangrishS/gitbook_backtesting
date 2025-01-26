import os
import re

def read_tree_from_log(log_file="/home/ubuntu/output.log"):
    """Read tree structure from log file."""
    try:
        with open(log_file, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: Log file not found.")
        return ""

def process_tree_string(tree_string):
    """Process tree string into hierarchical structure."""
    lines = tree_string.strip().splitlines()
    processed_lines = []
    for line in lines:
        depth = line.count('|') + line.count('├──')
        cleaned_line = re.sub(r'^[│├─\s]+', '', line).strip()
        processed_line = "#" * depth + " " + cleaned_line
        processed_lines.append(processed_line)
    
    return processed_lines

def create_content_files(processed_lines, base_dir="your-content"):
    """Create markdown files with hierarchical structure."""
    created_files = []
    
    for line in processed_lines:
        depth = line.count('#')
        title = line.lstrip('#').strip()
        
        filename = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-') + '.md'
        filepath = os.path.join(base_dir, filename)
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(f"{'#' * depth} {title}\n\n*Add content here*")
        
        created_files.append((depth, filename, title))
    
    return created_files

def generate_summary(created_files, base_dir="your-content"):
    """Generate SUMMARY.md outside content directory."""
    summary_lines = ["# Summary\n"]
    
    for depth, filename, title in created_files:
        indent = "  " * (depth - 1)
        summary_lines.append(f"{indent}- [{title}](your-content/{filename})")
    
    # Write SUMMARY.md in the parent directory
    summary_path = "SUMMARY.md"
    with open(summary_path, 'w') as f:
        f.write("\n".join(summary_lines))
    
    print("SUMMARY.md generated successfully!")

def main():
    tree_string = read_tree_from_log()
    
    if not tree_string:
        print("No tree data found. Exiting.")
        return
    
    processed_lines = process_tree_string(tree_string)
    created_files = create_content_files(processed_lines)
    generate_summary(created_files)

if __name__ == "__main__":
    main()
