import os
from urllib.parse import quote
import chardet  # 新增引入

EXCLUDE_DIRS = ['.git', 'docs', '.vscode', '.circleci', 'site','.github']
README_MD = ['README.md', 'readme.md', 'index.md']

TXT_EXTS = ['md', 'txt']
TXT_URL_PREFIX = 'https://github.com/Nagi-ovo/BJUT-Helper/blob/master/'
BIN_URL_PREFIX = 'https://github.com/Nagi-ovo/BJUT-Helper/raw/master/'


def list_files(course: str):
    filelist_texts = '## 文件列表\n\n'
    readme_path = ''
    for root, dirs, files in os.walk(course):
        files.sort()
        level = root.replace(course, '').count(os.sep)
        indent = ' ' * 4 * level
        filelist_texts += '{}- {}\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in README_MD:
                if f.split('.')[-1] in TXT_EXTS:
                    # 修改此处，使用 chardet 检测文件编码并指定正确的编码解决文档使用错误编码的问题。
                    with open('{}/{}'.format(root, f), 'rb') as file:
                        result = chardet.detect(file.read())
                        file_encoding = result['encoding']
                    filelist_texts += '{}- [{}]({})\n'.format(subindent,
                                                              f, TXT_URL_PREFIX + quote('{}/{}'.format(root, f)), encoding=file_encoding)
                else:
                    filelist_texts += '{}- [{}]({})\n'.format(subindent,
                                                              f, BIN_URL_PREFIX + quote('{}/{}'.format(root, f)))
            elif root == course and readme_path == '':
                readme_path = '{}/{}'.format(root, f)
    return filelist_texts, readme_path


def generate_md(course: str, filelist_texts: str, readme_path: str):
    final_texts = ['\n\n', filelist_texts]
    if readme_path:
        # 修改此处，使用 chardet 检测文件编码并指定正确的编码解决文档使用错误编码的问题。
        with open(readme_path, 'rb') as file:
            result = chardet.detect(file.read())
            file_encoding = result['encoding']
        with open(readme_path, 'r', encoding=file_encoding) as file:
            final_texts = file.readlines() + final_texts
    with open('docs/{}.md'.format(course), 'w') as file:
        file.writelines(final_texts)


if __name__ == '__main__':
    if not os.path.isdir('docs'):
        os.mkdir('docs')

    courses = list(filter(lambda x: os.path.isdir(x) and (
        x not in EXCLUDE_DIRS), os.listdir('.')))  # list courses

    for course in courses:
        filelist_texts, readme_path = list_files(course)
        generate_md(course, filelist_texts, readme_path)

    with open('README.md', 'r', encoding='utf-8') as file:
        mainreadme_lines = file.readlines()

    with open('docs/index.md', 'w', encoding='utf-8') as file:
        file.writelines(mainreadme_lines)