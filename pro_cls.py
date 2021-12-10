import math
import threading
import time
from queue import Queue
import requests
import json
from bs4 import BeautifulSoup

cls_txt = {}


def run(que):
    headers = {
        'Cookie': 'OCSSID=4df0bjva6j7ejussu8al3eqo03',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    cnt = 0
    while que.empty() is not True:
        try:
            url = que.get()
            name = url.split("term=")[-1]
            print(name)
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.content, "html.parser", from_encoding='gb18030')
            global cls_txt
            cls_txt[name] = json.loads(soup.text)
            time.sleep(1)
            cnt = cnt + 1
            print("完成第 %s 个" % (cnt))
        except Exception as e:
            print(e)


def prepare(result):
    queue = Queue()
    for obj in result:
        queue.put('https://relatedwords.org/api/related?term={}'.format(obj))
    for i in range(1, 6):
        t = threading.Thread(target=run, args=(queue,))
        t.start()
        t.join()
    with open("./all_cls_relation.json", 'w', encoding='utf-8') as fr:
        global cls_txt
        json.dump(cls_txt, fp=fr, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    with open("./cls_labels.txt", 'r', encoding='utf8') as fr:
        name = []
        for line in fr:
            str = line.split(",")
            for obj in str:
                name.append(obj.replace('\n', ''))
        prepare(name)
    cls_tab = {}

    range_up = 10
    with open("./all_cls_relation.json", 'r', encoding='utf8') as fr:
        dic = fr
        json_data = json.load(dic)
        for obj in json_data:
            val = []
            num = min(range_up, math.ceil(json_data[obj][0]["score"]))
            for word_data in json_data[obj]:
                word = word_data["word"]
                if len(val) == num: break
                val.append(word)
            cls_tab[obj] = val
    with open("./ent_types.json", 'w', encoding='utf8') as fw:
        json.dump(cls_tab, fp=fw, ensure_ascii=False, indent=4, sort_keys=False)
    with open("./ent_types.json", "r", encoding='utf8') as fr:
        print([obj for obj in json.load(fr)])
