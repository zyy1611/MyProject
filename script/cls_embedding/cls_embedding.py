import numpy as np
import torch
import json
import math


def glove_trans_vec(cls):
    cls_emdedding = {}
    with open('./glove.6B.300d.txt', 'r', encoding='utf—8') as fw:  # 以gbk编码读取
        for line in fw:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
        for obj in cls:
            zero = np.zeros(300, )
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
    return result


def read_word2vec(file_path, dim):
    print('\n', file_path)
    word2vec = dict()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip('\n').split(' ')
            if len(line) != dim + 1:
                continue
            try:
                v = np.array(list(map(float, line[1:])), dtype=np.float64)
                word2vec[line[0].lower()] = v
            except:
                continue
    file.close()
    return word2vec


def wiki_trans_vec(cls):
    word2vec = read_word2vec("./wiki-news-300d-1M.vec", 300)
    shape = [len(cls), 300]
    std = 1.0 / math.sqrt(shape[1])
    embeds = np.random.normal(scale=std, size=shape)
    cls_embedding = {}
    for idx in range(len(cls)):
        cls_embedding[cls[idx]] = embeds[idx]
        nns = cls[idx].split(' ')
        print(cls[idx], nns)
        for nn in nns:
            nn = nn.lower()
            if nn in word2vec.keys():
                cls_embedding[cls[idx]] += word2vec[nn]
    result = {}
    for obj in cls_embedding:
        result[obj] = cls_embedding[obj].tolist()
    return result


if __name__ == "__main__":
    embeddings_dict = {}
    cls = []
    with open("../process_cls/cls_labels.txt", 'r', encoding='utf8') as fr:
        for line in fr:
            str = line.split(",")
            for obj in str:
                cls.append(obj.replace('\n', ''))
        print(cls)
    # result = glove_trans_vec(cls)
    result = wiki_trans_vec(cls)
    print(result)
    with open('./cls_embedding_wiki.json', 'w', encoding='utf8') as fw:
        json.dump(result, fw, ensure_ascii=False, indent=4, sort_keys=False)
