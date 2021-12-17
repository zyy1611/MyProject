import threading
import time
from queue import Queue
import requests
import json
from bs4 import BeautifulSoup
import re

# 将正则表达式编译成Pattern对象
pattern = re.compile('<meta content=[",\']([\s\S]*)[",\'] property="og:description"/>')

# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None

des_txt = {}


def run(que):
    headers = {
        'Cookie': '_ga=GA1.1.910646490.1638951329; _ga_ZRJC7X9CNM=GS1.1.1639403430.2.0.1639403430.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    }
    proxies = {
        'https': '127.0.0.1:7078',  # 查找到你的vpn在本机使用的https代理端口
    }

    cnt = 0
    while que.empty() is not True:
        try:
            ent = que.get()
            id = ent[0]
            url = ent[1]
            print(url)
            res = requests.get(url, headers=headers, proxies=proxies)
            soup = BeautifulSoup(res.content, "html.parser", from_encoding='gb18030')
            met = soup.find('meta', property="og:description")
            match = pattern.findall(str(met))
            global des_txt
            des_txt[id] = match
            print("---->")
            for obj in des_txt:
                print(obj, des_txt[obj])
            time.sleep(2)
            cnt = cnt + 1
            print("完成第 %s 个" % (cnt))
        except Exception as e:
            print(e)


def prepare(result):
    queue = Queue()
    for obj in result:
        queue.put([obj, result[obj]])
    for i in range(1, 6):
        t = threading.Thread(target=run, args=(queue,))
        t.start()
        t.join()
    with open("./all_cls_relation.json", 'w', encoding='utf-8') as fr:
        global des_txt
        json.dump(des_txt, fp=fr, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    with open("./fr_en_extra.json", 'r', encoding='utf8') as fr:
        url = {}
        json_data = json.load(fr)
        for obj in json_data:
            if json_data[obj].split("//")[1].find("fr.") != -1:
                continue
            url[int(obj)] = (json_data[obj])
    prepare(url)
    print(des_txt)
