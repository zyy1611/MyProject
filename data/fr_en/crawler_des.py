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
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Proxy - Connection': 'keep - alive',
        'Cookie': 'dbpv_has_js=1; dbpv_primary_lang=fr; _ga=GA1.1.910646490.1638951329; _ga_ZRJC7X9CNM=GS1.1.1639403430.2.0.1639403430.0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    proxies = {
        'https': '127.0.0.1:7080',  # 查找到你的vpn在本机使用的https代理端口
    }
    cnt = 0
    while que.empty() is not True:
        try:
            ent = que.get()
            id = ent[0]
            url = "http://fr.dbpedia.org/page/{}".format(ent[1])
            print(url)
            res = requests.get(url, headers=headers, proxies=proxies)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.content, "html.parser", from_encoding='utf8')
            content = soup.find('p').get_text()
            global des_txt
            des_txt[id] = content
            print("---->")
            for obj in des_txt:
                print(obj, des_txt[obj])
            time.sleep(2)
            cnt = cnt + 1
            print("完成第 %s 个" % (cnt))
        except Exception as e:
            print(e)


def fill_fr_extra():
    ent_name = {}
    with open('./ent_ids_1', 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            ent_name[int(th[0])] = th[1].split('/')[-1]

    with open('./extra_fr_des.json', 'r', encoding='utf8') as fr:
        json_data = json.load(fr)
        none = []
        for obj in json_data:
            if json_data[obj] == "none" or len(json_data[obj]) == 0: none.append(obj)
    ent_tab = {}
    for obj in none:
        ent_tab[obj] = ent_name[int(obj)]
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Cookie': 'WMF-Last-Access=21-Dec-2021; WMF-Last-Access-Global=21-Dec-2021; GeoIP=HK:HCW:Central:22.29:114.15:v4; frwikimwuser-sessionId=6bd20024cb880f4e7176; frwikiwmE-sessionTickLastTickTime=1640070364782; frwikiwmE-sessionTickTickCount=34; frwikiel-sessionId=8b2f5aeab9953f3e601b',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    proxies = {
        'https': '127.0.0.1:7080',  # 查找到你的vpn在本机使用的https代理端口
    }
    for id in ent_tab:
        try:
            url = "https://fr.wikipedia.org/wiki/{}".format(ent_tab[id])
            res = requests.get(url, headers=headers, proxies=proxies)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.content, "html.parser", from_encoding='utf8')
            content = soup.find_all('p')
            for obj in content:
                if len(obj.find_all('b')) > 0 and len(obj.find_all('a')) > 0:
                    str = obj.get_text().replace("\n", "")
            json_data[id] = str
            print(id, '-->', ent_tab[id], '-->', str)
        except Exception as e:
            print(e)
        time.sleep(2)
    print(len(json_data))
    with open("./extra_fr_des.json", 'w', encoding='utf-8') as fr:
        json.dump(json_data, fp=fr, ensure_ascii=False, indent=4, sort_keys=False)


def refer_run(que):
    # step1:指定Url
    headers = {
        'Cookie': 'dbpv_has_js=1; dbpv_primary_lang=fr; _ga=GA1.1.910646490.1638951329; _ga_ZRJC7X9CNM=GS1.1.1639403430.2.0.1639403430.0',
        'Host': 'fr.dbpedia.org',
        'Origin': 'http://fr.dbpedia.org',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    }
    proxies = {
        'https': '127.0.0.1:7080',  # 查找到你的vpn在本机使用的https代理端口
    }
    cnt = 0
    url = "http://fr.dbpedia.org/sparql"

    while que.empty() is not True:
        try:
            ent = que.get()
            id = ent[0]
            ent_name = ent[1]
            headers["Referer"] = 'http://fr.dbpedia.org/page/{}'.format(ent_name)
            print(headers["Referer"])
            query = "SELECT DISTINCT ?hasprop ?v where { <http://fr.dbpedia.org/resource/" + ent_name + "> ?hasprop ?v}"
            data = {'default-graph-uri': 'http://fr.dbpedia.org',
                    'query': query}
            page_text = requests.post(url=url, headers=headers, proxies=proxies, data=data)
            page_text.encoding = 'gbk'
            soup = BeautifulSoup(page_text.content, "html.parser", from_encoding='utf8')
            if len(soup.find_all(name="literal", attrs={'xml:lang': 'fr'})) == 0:
                content = "none"
            else:
                content = soup.find_all(name="literal", attrs={'xml:lang': 'fr'})[-1].get_text()
            global des_txt
            des_txt[id] = content
            print("---->")
            print(id, content)
            time.sleep(2)
            cnt = cnt + 1
            print("完成第 %s 个" % (cnt))
        except Exception as e:
            print(e)


def prepare(result, second=False):
    queue = Queue()
    for obj in result:
        queue.put([obj, result[obj]])
    for i in range(1, 6):
        if second is True:
            t = threading.Thread(target=refer_run, args=(queue,))
        else:
            t = threading.Thread(target=run, args=(queue,))
        t.start()
        t.join()
    with open("./extra_fr_des.json", 'w', encoding='utf-8') as fr:
        global des_txt
        print(len(des_txt))
        json.dump(des_txt, fp=fr, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    # done_ids = []
    # with open("./extra_fr_des.json", 'r', encoding='utf-8') as fr:
    #     json_des = json.load(fr)
    #     for obj in json_des:
    #         done_ids.append(obj)
    # fr.close()
    # des_txt = json_des
    # print(len(des_txt))
    # with open("./fr_en_extra.json", 'r', encoding='utf8') as fr:
    #     url = {}
    #     json_data = json.load(fr)
    #     for obj in json_data:
    #         if json_data[obj].split("//")[1].find("fr.") == -1:
    #             continue
    #         if des_txt.get(obj) is not None and len(des_txt[obj]) > 0: continue
    #         ent_name = json_data[obj].split('/')[-1]
    #         url[int(obj)] = ent_name
    # prepare(url, True)
    fill_fr_extra()
#             30095
