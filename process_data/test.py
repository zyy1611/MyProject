import json

cnt = {}
with open("./fr_en/2_typing_result.json", 'r', encoding='utf8') as fr:
    json_data = json.load(fr)
    for obj in json_data:
        if cnt.get(json_data[obj]) is None:
            cnt[json_data[obj]] = 1
        cnt[json_data[obj]] = cnt[json_data[obj]] + 1
    for obj in cnt:
        print(obj, cnt[obj])
