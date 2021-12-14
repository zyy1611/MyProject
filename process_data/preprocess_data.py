import os
import json


def delete_sub(text_obj):
    pos = [text_obj.find(" is "), text_obj.find(" was "), text_obj.find(" are "), text_obj.find(" were ")]
    for obj in pos:
        if obj > 0:
            return text_obj[obj:]


class ReplaceSub(object):
    def __init__(self, dataset, comment_index, des_data, link_data):
        self.dataset = dataset
        self.comment_index = comment_index
        self.des_data = des_data
        self.link_data = link_data
        self.result = {}
        self.cnt = 0

    def process(self):
        for ent_id in self.des_data:
            text_obj = self.des_data[ent_id]
            del_sub = delete_sub(text_obj)
            if del_sub is None:
                self.cnt = self.cnt + 1
                print(self.cnt)
                self.result[ent_id] = {"ent_name": self.link_data[ent_id],
                                       "description": text_obj}
            else:
                self.result[ent_id] = {"ent_name": self.link_data[ent_id],
                                       "description": self.link_data[ent_id] + del_sub}
        print(len(self.result))
        try:
            with open("../process_data/{}/comment_{}_description.json".format(self.dataset, self.comment_index), 'w',
                      encoding='utf-8') as fw:
                json.dump(self.result, fw, ensure_ascii=False, indent=4, sort_keys=False)
                fw.close()
        except Exception as e:
            print("写入失败", e)


class process_id(object):
    def __init__(self, data):
        self.data = data

    def process(self):
        pass


def get_name(dataset, comment_index):
    ent_name = {}
    with open('../data/{}/ent_ids_{}'.format(dataset, comment_index), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            ent_name[int(th[0])] = th[1].split('/')[-1]
    for obj in ent_name:
        print(ent_name[obj])
    return ent_name


def replace_sub(dataset, comment_index):
    ent_des = {}
    with open('../data/{}/comment_{}'.format(dataset, comment_index), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            ent_des[int(th[0])] = th[1]
    fr.close()
    for obj in ent_des:
        if ent_des[obj].find(" is ") > -1 or ent_des[obj].find(" was ") > -1 or ent_des[obj].find(" are ") > -1 or \
                ent_des[obj].find(" were ") > 0:
            continue
        print(obj, ent_des[obj])
    ent_name = get_name(dataset, comment_index)
    fr.close()
    # for obj in ent_name:
    #     print(obj, ent_name[obj])
    replacer = ReplaceSub(dataset, comment_index, ent_des, ent_name)
    replacer.process()


def check(str):
    for obj in str:
        if obj not in "0123456789":
            return True
    return False


def check_2(str):
    res = ""
    for obj in str:
        if obj in "0123456789":
            res += obj
    return res


def process_id():
    list1 = []
    list2 = []
    id_des = {}
    with open('./comment_1_eng2.txt', 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            id_des[th[1]] = th[0]
            if check(th[0]) or len(th[0]) == 0:
                list1.append(th[1])
            else:
                list2.append(th[1])
    print(len(list1), len(list2))
    ids = [10301, 5, 7944, 4225, 3218, 23380, 8119, 10028, 24499, 4012, 758, 6294, 5366, 1247, 3369, 2488, 2947]
    for obj in list1:
        if check_2(id_des[obj]) == "":
            pass
        else:
            ids.append(check_2(id_des[obj]))
    print(len(ids))
    dataset = "fr_en"
    comment_index = "comment_1"
    ent_des = {}
    load_content = []
    with open('../data/{}/{}'.format(dataset, comment_index), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            ent_des[int(th[0])] = th[1]
    return ids


def generate_des(ids):
    que = []
    ent_des = []
    with open("./sepecil_2l.txt", 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            que.append(th[0])
    cnt = 0
    with open('./comment_1_eng2.txt', 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            try:
                ent_des.append(str(int(th[0])) + '\t' + th[1])
            except:
                ent_des.append(str(int(ids[cnt])) + '\t' + que[cnt])
                cnt = cnt + 1
    for obj in ent_des:
        print(obj)
    with open('./fr_en/fr_to_eng.txt', 'w') as fw:
        for obj in ent_des:
            fw.write(obj + '\n')
    fw.close()


def get_eng_name(dataset):
    id = []
    name = []
    with open("../data/{}/ent_ids_1".format(dataset), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split("\t")
            id.append(th[0])
    with open("./{}/ent_name.txt".format(dataset), 'r', encoding='utf8') as fr:
        for line in fr:
            name.append(line[:-1].replace(' ', ''))
    ent_name = dict(zip(id, name))
    print(ent_name)
    return ent_name


def generate_comment(ent_tab, dataset):
    result = {}
    cnt = 0
    with open("./{}_en/{}_to_eng.txt".format(dataset, dataset), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split("\t")
            del_sub = delete_sub(th[1])
            if del_sub is None:
                cnt = cnt + 1
                print(cnt)
                result[th[0]] = {"ent_name": ent_tab[th[0]], "description": th[1]}
            else:
                result[th[0]] = {"ent_name": ent_tab[th[0]], "description": ent_tab[th[0]] + del_sub}
    print(len(result))
    try:
        with open("./{}_en/comment_1_description.json".format(dataset), 'w',
                  encoding='utf-8') as fw:
            json.dump(result, fw, ensure_ascii=False, indent=4, sort_keys=False)
            fw.close()
    except Exception as e:
        print("写入失败", e)


if __name__ == "__main__":
    replace_sub("fr_en", "2")  # 将数据集中英文版本的实体描述的主语换成对应的名字,并写入文件中
    # ids = process_id()  # 将翻译之后的法语数据文本进行id清洗
    # generate_des(ids)  # 将清洗后id和description写入最终文本中
    # ent_tab = get_eng_name("fr_en")  # 将翻译之后的法语->英语实体名进行id映射，返回字典{id,ent_eng_name}
    # generate_comment(ent_tab, "fr")  # 生成替换掉主语的实体文本，并写入文件zhong
