import json
from textwrap import indent

# json文件读取


def read_json(path):
    for en in ['utf8', 'gb18030']:
        try:
            with open(path, 'r', encoding=en) as f:
                data = json.load(f)
            return data
        except Exception as e:
            # print('read json error:',e)
            pass


def write_json(path, dic):
    with open(path, 'w') as f:
        json.dump(dic, f, indent='    ', ensure_ascii=False)
