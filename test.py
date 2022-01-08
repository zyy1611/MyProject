from openprompt.data_utils import InputExample
from openprompt.prompts import ManualTemplate
from openprompt.prompts import ManualVerbalizer
from openprompt import PromptForClassification
from openprompt import PromptDataLoader
from openprompt.plms import load_plm
import torch
import json

classes = ['person', 'organization', 'location', 'buildings', 'arts', 'product', 'event', "other"]

data_set = "fr_en"
language_type = ["1", "2"]
for lt in language_type:
    with open("./process_data/{}/comment_{}_description.json".format(data_set, lt), 'r',
              encoding='utf8') as fr:
        json_data = json.load(fr)
        fr.close()
    dataset = []
    pos = 0
    for obj in json_data:
        des_str = json_data[obj]["description"].replace(json_data[obj]["ent_name"],
                                                        "???")
        point_pos = des_str.find(".")
        des_str_front = des_str[:point_pos + 1]
        des_str_tail = des_str[point_pos + 1:]

        dataset.append(InputExample(guid=0, label=int(obj),

                                    meta={"des_str_front": des_str_front, "des_str_tail": des_str_tail,
                                          "ent": "???"}))
        pos = pos + 1
    plm, tokenizer, model_config, WrapperClass = load_plm("bert", "bert-base-uncased")
    promptTemplate = ManualTemplate(
        text='{"meta":"des_str_front"}.{"meta": "ent"} is {"mask"}.{"meta":"des_str_tail"}',
        tokenizer=tokenizer,
    )

    promptVerbalizer = ManualVerbalizer(
        classes=classes,
        label_words={
            "person": [
                "sportsman",
                "singer",
                "actor",
                "politician",
                "worker",
                "royal",
                "minister",
                "human",
                "cosmonaut"
            ],
            "organization": [
                "organization",
                "establishment",
                "federation",
                "institution",
                "union",
                "army",
                "company",
                "sports team"
            ],
            "location": [
                "location",
                "political party",
                "country",
                "region",
                "placement",
                "mountain",
                "body of water",
                "city",
                "island",
                "park"
            ],
            "buildings": [
                "buildings",
                "school",
                "hospital",
                "airport",
                "roof",
                "stadium",
                "architecture",
                "government"
            ],
            "arts": [
                "movie",
                "music",
                "broadcast",
                "video game"
            ],
            "product": [
                "brand",
                "airplane",
                "car",
                "train"
            ],
            "event": [
                "war",
                "disaster",
                "competition",
                "festival",
            ],
            "other": [
                "language",
                "award",
                "disease"
            ]
        },
        tokenizer=tokenizer,
    )
    promptModel = PromptForClassification(
        template=promptTemplate,
        plm=plm,
        verbalizer=promptVerbalizer,
    )

    data_loader = PromptDataLoader(
        dataset=dataset,
        tokenizer=tokenizer,
        template=promptTemplate,
        tokenizer_wrapper_class=WrapperClass,
    )
    promptModel.eval()
    typing_res = {}
    cnt = 1
    failed_ids = {"1": [], "2": []}
    with torch.no_grad():
        for batch in data_loader:
            try:
                logits = promptModel(batch)
                preds = torch.argmax(logits, dim=-1)
                print(batch["label"].item(), classes[preds], "   第{}个分类完成.".format(cnt))
                typing_res[batch["label"].item()] = classes[preds]
            except Exception as e:
                print(e, "   第{}个分类失败，标号{}".format(cnt, batch["label"].item()))
                failed_ids[lt].append(batch["label"].item())
            cnt = cnt + 1

    with open("./process_data/{}/{}_typing_result.json".format(data_set, lt), 'w', encoding='utf8') as fw:
        json.dump(typing_res, fp=fw, indent=4, ensure_ascii=False, sort_keys=False)
    print(failed_ids)
