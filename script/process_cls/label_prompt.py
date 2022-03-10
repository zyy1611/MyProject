import json
import torch
import torch.nn as nn
from transformers import BertForMaskedLM, BertConfig, BertTokenizer
import numpy as np
import heapq

config_path = "../../raw_bert/bert-base-uncased/config.json"
config = BertConfig.from_pretrained(config_path)  # 导入模型超参数
vocab_path = r"../../raw_bert/bert-base-uncased/vocab.txt"
tokenizer = BertTokenizer.from_pretrained("../../raw_bert/bert-base-uncased")
vocab_tab = {}
cnt = 0
with open(vocab_path, "r", encoding='utf-8') as f:
    for line in f.readlines():
        vocab_tab[cnt] = line[:-1]
        cnt = cnt + 1


class Bert_Model(nn.Module):
    def __init__(self, bert_path, config_file):
        super(Bert_Model, self).__init__()
        self.bert = BertForMaskedLM.from_pretrained(bert_path, config=config_file)  # 加载预训练模型权重

    def forward(self, input_ids, attention_mask, token_type_ids):
        outputs = self.bert(input_ids, attention_mask, token_type_ids)
        logit = outputs[0]  # 池化后的输出 [bs, config.hidden_size]

        return logit


model = Bert_Model(bert_path=r"../../raw_bert/bert-base-uncased/pytorch_model.bin", config_file=config)

model.eval()


def pre(text, maskpos):
    encode_dict = tokenizer.encode_plus(text, max_length=50, padding='max_length', truncation=True)
    id = encode_dict["input_ids"]
    inputid = id[:]
    inputid[maskpos] = tokenizer.mask_token_id
    attid = encode_dict["attention_mask"]
    segmentid = encode_dict["token_type_ids"]
    inputid = torch.from_numpy(np.array([inputid])).long()
    attid = torch.from_numpy(np.array([attid])).long()
    segmentid = torch.from_numpy(np.array([segmentid])).long()
    out_test = model(inputid, attid, segmentid)
    tout_train_mask = out_test[:, maskpos, :].detach().numpy()[0]
    index_li = heapq.nlargest(8, range(len(tout_train_mask)), tout_train_mask.take)
    # pos = tout_train_mask.argmax(axis=1)
    return [vocab_tab[obj] for obj in index_li]


onto = []
res = {}
with open("./cls_label_ontoEA.txt", 'r', encoding='utf-8') as fr:
    for line in fr:
        onto.append(line.strip())
failed=[]
for obj in onto:
    try:
        text = '{} and [MASK] are the same.'.format(obj)
        val = pre(text, 2 + len(obj.split(' ')))
        res[obj] = val
        print(obj, "==", val)
    except Exception as e:
        failed.append(obj)
with open("./onto_mapping_bert.json", 'w', encoding='utf-8') as fw:
    json.dump(res, fw, ensure_ascii=False, indent=4, sort_keys=False)
