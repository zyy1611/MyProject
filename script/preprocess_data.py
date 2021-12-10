import os
import json


class replace_sub(object):
    def __init__(self, dataset, comment_index, des_data, link_data):
        self.dataset = dataset
        self.comment_index = comment_index
        self.des_data = des_data
        self.link_data = link_data
        self.result = {}
        self.cnt = 0

    def delete_sub(self, text_obj):
        pos = [text_obj.find(" is "), text_obj.find(" was "), text_obj.find(" are "), text_obj.find(" were ")]
        for obj in pos:
            if obj > 0:
                return text_obj[obj:]

    def process(self):
        for ent_id in self.des_data:
            text_obj = self.des_data[ent_id]
            del_sub = self.delete_sub(text_obj)
            if del_sub is None:
                self.cnt = self.cnt + 1
                print(self.cnt)
                continue
            self.result[ent_id] = {"ent_name": self.link_data[ent_id], "description": self.link_data[ent_id] + del_sub}
        print(len(self.result))
        try:
            with open("../process_data/{}/{}_description.json".format(self.dataset, self.comment_index), 'w',
                      encoding='utf-8') as fw:
                fw.write(json.dumps(self.result, ensure_ascii=False))
                fw.close()
        except Exception as e:
            print("写入失败", e)


if __name__ == "__main__":
    ent_des = {}
    ent_name = {}
    dataset = "fr_en"
    comment_index = "comment_2"
    link_index = "ent_ids_2"
    with open('../data/{}/{}'.format(dataset, comment_index), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            ent_des[int(th[0])] = th[1]
    fr.close()
    for obj in ent_des:
        if ent_des[obj].find(" is ") > -1 or ent_des[obj].find(" was ") > -1 or ent_des[obj].find(" are ") > -1 or \
                ent_des[obj].find(" were ") > 0:
            continue
        print(obj, ent_des[obj])
    with open('../data/{}/{}'.format(dataset, link_index), 'r', encoding='utf8') as fr:
        for line in fr:
            th = line[:-1].split('\t')
            ent_name[int(th[0])] = th[1].split('/')[-1]
    fr.close()
    # for obj in ent_name:
    #     print(obj, ent_name[obj])
    replacer = replace_sub(dataset, comment_index, ent_des, ent_name)
    replacer.process()
