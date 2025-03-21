# -*- coding: utf-8 -*-

import os
from urllib.parse import quote

EXCLUDE_DIRS = ['.git', 'docs', '.vscode', '.circleci', 'site','.github','src','overrides','images']
README_MD = ['README.md', 'readme.md', 'index.md']

TXT_EXTS = ['md', 'txt']
TXT_URL_PREFIX = 'https://github.com/bjut-swift/BJUT-Helper/blob/master/'
BIN_URL_PREFIX = 'https://github.com/bjut-swift/BJUT-Helper/raw/master/'


def list_files(course: str):
    filelist_texts = '## 文件列表\n\n'
    readme_path = ''
    for root, dirs, files in os.walk('./' + course):
        files.sort()
        level = root.replace('./' + course, '').count(os.sep)
        indent = ' ' * 4 * level
        subindent = ' ' * 4 * (level + 1)

        if root != './' + course:  # For subdirectories
            filelist_texts += '{}- {}\n\n'.format(indent, os.path.basename(root))
        else:  # For the top-level directory (course directory itself)
            filelist_texts += '- {}\n\n'.format(os.path.basename(root))

        for f in files:
            if f not in README_MD:
                ext = f.split('.')[-1]
                file_path = os.path.join(root, f).replace('./', '')  # Remove './' from path
                if ext in TXT_EXTS:
                    if ext == 'md':
                        filelist_texts += '{}- [{}]({})\n\n'.format(subindent, f, TXT_URL_PREFIX + quote(file_path))
                    else:
                        filelist_texts += '{}- [{}]({})\n\n'.format(subindent, f, TXT_URL_PREFIX + quote(file_path))
                else:
                    filelist_texts += '{}- [{}]({})\n\n'.format(subindent, f, BIN_URL_PREFIX + quote(file_path))
            elif root == './' + course and readme_path == '':
                readme_path = os.path.join(root, f)

    return filelist_texts, readme_path


def generate_md(course: str, filelist_texts: str, readme_path: str):
    final_texts = ['\n\n', filelist_texts]
    if readme_path:
        with open(readme_path, 'r', encoding='utf-8') as file:
            final_texts = file.readlines() + final_texts
    with open('docs/{}.md'.format(course), 'w', encoding='utf-8') as file:
        file.writelines(final_texts)


if __name__ == '__main__':
    if os.path.exists('docs'):
        shutil.rmtree('docs')
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
