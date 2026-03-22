import pandas as pd
import re
import os
from glob import glob

# 读取 .md 文件
def read_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 解析三级标题及其内容
def parse_md_content(text):
    pattern = re.compile(r'([A-Za-z]?\d+(?:\.\d+)+(?:-\d+)?)(.*?)(?=\n[A-Za-z]?\d+(?:\.\d+)+(?:-\d+)?|\Z)', re.DOTALL)
    matches = pattern.findall(text)
    html_table_pattern = re.compile(r'<table>.*?</table>', re.DOTALL)

    all_items = [(title.strip(), content.strip()) for title, content in matches]

    # 找出父标题有子标题
    parent_with_subs = set()
    for title, _ in all_items:
        if '-' in title:
            parent = title.split('-')[0]
            parent_with_subs.add(parent)

    text_items = []
    table_items = []

    for title, content in all_items:
        # 忽略有子标题的父标题
        if '-' not in title and title in parent_with_subs:
            continue

        html_tables = html_table_pattern.findall(content)
        non_html_content = html_table_pattern.sub('', content).strip()

        if non_html_content:
            text_items.append({"标题": title, "内容": non_html_content})

        for table in html_tables:
            table_items.append({"标题": title, "内容": table})

    return text_items, table_items

# 保存到 Excel 文件
def save_to_excel(text_items, table_items, output_file):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with pd.ExcelWriter(output_file) as writer:
        if text_items:
            pd.DataFrame(text_items).to_excel(writer, sheet_name="Text", index=False)
        if table_items:
            pd.DataFrame(table_items).to_excel(writer, sheet_name="Tables", index=False)

# 主函数：单文件或文件夹模式
def md_to_excel(path):
    if os.path.isfile(path) and path.lower().endswith('.md'):
        md_files = [path]
    elif os.path.isdir(path):
        md_files = glob(os.path.join(path, '*.md'))
    else:
        print(f"路径无效或不是 md 文件: {path}")
        return

    for md_file_path in md_files:
        text = read_md_file(md_file_path)
        text_items, table_items = parse_md_content(text)

        base_name = os.path.splitext(os.path.basename(md_file_path))[0]
        excel_folder = os.path.join('files_revision', 'Excel')
        excel_file_path = os.path.join(excel_folder, base_name + '.xlsx')

        save_to_excel(text_items, table_items, excel_file_path)
        print(f"[完成] {md_file_path} → {excel_file_path}")

# 示例调用
if __name__ == "__main__":
    # 可以替换为单个文件路径或文件夹路径
    path = r"D:\PycharmProjects\Fourth_lunwen\Document_interpretation\files_revision"
    md_to_excel(path)