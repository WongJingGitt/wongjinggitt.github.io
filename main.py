import json
import os
from datetime import datetime
from os import path
import subprocess


class Push:

    def __init__(self):
        self._root_path = path.abspath(path.dirname(__file__))
        self._config_path = path.join(self._root_path, 'config')
        self._blog_path = path.join(self._root_path, 'blog')
        self.__walker()
        self.__update()

    def __walker(self):
        hierarchy = {
            "type": "directory",
            "name": "blog",
            "path": "",
            "children": []
        }

        for root, dirs, files in os.walk(self._blog_path):
            current_dir = hierarchy
            rel_path = os.path.relpath(root, self._blog_path)
            if rel_path != ".":
                sub_dirs = rel_path.split(os.sep)
                for sub_dir in sub_dirs:
                    found = False
                    for child in current_dir["children"]:
                        if child["name"] == sub_dir:
                            current_dir = child
                            found = True
                            break
                    if not found:
                        new_dir = {
                            "type": "directory",
                            "name": sub_dir,
                            "path": os.path.join(current_dir["path"], sub_dir),  # 更新相对路径
                            "children": []
                        }
                        current_dir["children"].append(new_dir)
                        current_dir = new_dir

            for file in files:
                current_dir["children"].append({
                    "type": "file",
                    "name": file,
                    "path": os.path.join(current_dir["path"], file)  # 更新相对路径
                })

        with open('config/blog_list.json', 'w', encoding='utf-8') as fw:
            json.dump(hierarchy, fw, ensure_ascii=False)
            fw.close()

    def __update(self):
        subprocess.run(['git', 'pull', 'origin', 'main'])
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        subprocess.run(['git', 'push', '-u', 'origin', 'main'])


if __name__ == '__main__':
    p = Push()