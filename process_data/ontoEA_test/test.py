# # cls_set = set()
# # with open("./crossview_link_1", 'r', encoding="utf-8") as fr:
# #     for line in fr:
# #         line = line.strip().split('\t')
# #         type = line[1].split('/')[-1]
# #         cls_set.add(type)
# # with open("./crossview_link_2", 'r', encoding="utf-8") as fr:
# #     for line in fr:
# #         line = line.strip().split('\t')
# #         type = line[1].split('/')[-1]
# #         cls_set.add(type)
# # for obj in cls_set:
# #     print(obj)
# # tab={}
# # cls_list = [obj for obj in cls_set]
# # for obj in cls_set:
# #     tab[obj]=[obj.lower()]
# # print(cls_list)
# # print(tab)
# ent={}
# with open("../../data/fr_en_v1/ent_ids_1",'r',encoding='utf-8') as fr:
#     for line in fr:
#         line = line.strip().split('\t')
#         ent[line[1]]=line[0]
# with open("../../data/fr_en_v1/ent_ids_2",'r',encoding='utf-8') as fr:
#     for line in fr:
#         line = line.strip().split('\t')
#         ent[line[1]]=line[0]
# test_pair=[]
# with open("./train_links",'r',encoding='utf-8') as fr:
#     for line in fr:
#         line = line.strip().split('\t')
#         test_pair.append([int(ent[line[0]]),int(ent[line[1]])])
# print(test_pair)
str="entity is a genre of rock that appeared in the mid-1960s mainly in the United States and the United Kingdom."
print(len(str))