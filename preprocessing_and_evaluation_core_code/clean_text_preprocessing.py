import os
import re
from glob import glob

def is_formula_line(line):
    line_stripped = line.strip()
    if line_stripped.startswith('$$') or line_stripped.endswith('$$'):
        return True
    if '\\tag' in line:
        return True
    math_commands = [r'\\mathrm', r'\\sqrt', r'\\frac', r'\\sum', r'\\int',
                     r'\\alpha', r'\\beta', r'\\gamma', r'\\sin', r'\\cos',
                     r'\\tanh', r'\\cosh', r'\\sinh']
    for cmd in math_commands:
        if re.search(cmd, line):
            return True
    return False

def is_table_or_figure_line(line):
    line_stripped = line.strip()
    return line_stripped.startswith('表') or line_stripped.startswith('图')

def format_text(text):
    lines = text.split('\n')
    result = []
    current_parent = None
    parent_content = []

    for line in lines:
        if is_table_or_figure_line(line) or is_formula_line(line):
            if current_parent:
                parent_content.append(line)
            else:
                result.append(line)
            continue

        parent_match = re.match(r'([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(.*)', line)
        if parent_match:
            if current_parent:
                combined_content = '\n'.join(parent_content).strip()
                result.append(f"{current_parent}\t{combined_content}")
            current_parent = parent_match.group(1)
            first_line_content = parent_match.group(2).strip()
            parent_content = [first_line_content] if first_line_content else []
        else:
            if current_parent:
                parent_content.append(line.strip())
            else:
                result.append(line.strip())

    if current_parent:
        combined_content = '\n'.join(parent_content).strip()
        result.append(f"{current_parent}\t{combined_content}")

    return '\n'.join(result)

def read_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"文件读取失败: {filename}, {e}")
        return None

def write_to_file(text, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"文件写入失败: {filename}, {e}")

def process_path(path):
    if os.path.isfile(path) and path.lower().endswith('.md'):
        md_files = [path]
    elif os.path.isdir(path):
        md_files = glob(os.path.join(path, '*.md'))
    else:
        print(f"路径无效或不是 md 文件: {path}")
        return

    output_folder = 'files_revision'
    for md_file in md_files:
        text = read_from_file(md_file)
        if text:
            formatted_text = format_text(text)
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            output_filename = os.path.join(output_folder, base_name + '_text.md')
            write_to_file(formatted_text, output_filename)
            print(f"[完成] {md_file} → {output_filename}")

if __name__ == "__main__":
    # 可以是单个文件，也可以是文件夹
    path = r"D:\BaiduSyncdisk\科研论文撰写\小论文4\工程规范文件_revision\Markdown_clean"
    process_path(path)