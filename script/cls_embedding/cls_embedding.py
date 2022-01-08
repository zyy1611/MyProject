import numpy as np
import torch
import json

embeddings_dict = {}
cls = []
cls_emdedding = {}
with open("../process_cls/cls_labels_2.txt", 'r', encoding='utf8') as fr:
    for line in fr:
        str = line.split(",")
        for obj in str:
            cls.append(obj.replace('\n', ''))
    print(cls)
with open('./glove.6B.300d.txt', 'r', encoding='utf—8') as fw:  # 以gbk编码读取
    for line in fw:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], "float32")
        embeddings_dict[word] = vector
    for obj in cls:
        zero = np.zeros(300,)
        if obj not in embeddings_dict:
            for one in obj.split(" "):
                zero = zero + embeddings_dict[one]
            zero = zero / len(obj.split(" "))
            cls_emdedding[obj] = zero
        else:
            cls_emdedding[obj] = embeddings_dict[obj]
result = {}
for obj in cls_emdedding:
    result[obj] = cls_emdedding[obj].tolist()
with open('./cls_embedding.json', 'w', encoding='utf8') as fw:
    json.dump(result, fw, ensure_ascii=False, indent=4, sort_keys=False)
