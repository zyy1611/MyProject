from openprompt.data_utils import InputExample
from openprompt.prompts import ManualTemplate
from openprompt.prompts import ManualVerbalizer
from openprompt import PromptForClassification
from openprompt import PromptDataLoader
from openprompt.plms import load_plm
import torch
import json

classes = ['sportsman', 'singer', 'actor', 'politician', 'royal', 'cosmonaut', 'country', 'city', 'brand', 'airplane',
           'car', 'train', 'club', 'sports team', 'company', 'army', 'mall', 'school', 'hospital', 'airport', 'stadium',
           'government', 'body of water', 'mountain', 'park', 'island', 'movie', 'music', 'broadcast', 'video game',
           'war', 'disaster', 'competition', 'festival', 'language', 'award', 'disease']

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
            "sportsman": [
                "sportsman",
                "sport",
                "sportswoman",
                "athlete",
                "amateur",
                "sportsperson",
                "footballer",
                "jock"
            ],
            "singer": [
                "singer",
                "song",
                "vocalist",
                "opera",
                "soprano",
                "vocal range",
                "music",
                "jazz"
            ],
            "actor": [
                "actor",
                "comedy",
                "barrymore",
                "mime",
                "actress",
                "drama",
                "thespian",
                "doer"
            ],
            "politician": [
                "politician",
                "leader",
                "minister",
                "democrat",
                "candidate",
                "statesman",
                "legislator"
            ],
            "royal": [
                "royal",
                "imperial",
                "noble",
                "king",
                "regal",
                "queen",
                "monarch",
                "prince"
            ],
            "cosmonaut": [
                "cosmonaut",
                "yuri gagarin",
                "astronaut",
                "valentina tereshkova",
                "soviet union",
                "spaceman",
                "spacecraft",
                "gagarin"
            ],
            "country": [
                "country",
                "nation",
                "state",
                "land",
                "fatherland",
                "malta",
                "homeland",
                "region"
            ],
            "city": [
                "city",
                "metropolis",
                "town",
                "municipality",
                "urban",
                "suburb",
                "municipal",
                "megalopolis"
            ],
            "brand": [
                "brand",
                "mark",
                "label",
                "trademark",
                "advertising",
                "logo",
                "marketing",
                "blade"
            ],
            "airplane": [
                "airplane",
                "plane",
                "airliner",
                "propeller",
                "monoplane",
                "fuselage",
                "jet",
                "biplane"
            ],
            "car": [
                "car",
                "bus",
                "motor vehicle",
                "wheel",
                "automobile",
                "auto",
                "minivan",
                "suv"
            ],
            "train": [
                "train",
                "prepare",
                "locomotive",
                "develop",
                "educate",
                "groom",
                "railcar",
                "freight train"
            ],
            "club": [
                "club",
                "bludgeon",
                "golf club",
                "nightclub",
                "cudgel",
                "truncheon",
                "baton",
                "gather"
            ],
            "sports team": [
                "sports team",
                "team",
                "sport",
                "lacrosse"
            ],
            "company": [
                "company",
                "business",
                "corporation",
                "subsidiary",
                "companion",
                "troupe",
                "accompany",
                "unit"
            ],
            "army": [
                "army",
                "military",
                "soldier",
                "militia",
                "conscription",
                "infantry",
                "war machine",
                "regular army"
            ],
            "mall": [
                "mall",
                "shopping mall",
                "plaza",
                "shop",
                "strip mall",
                "center",
                "downtown",
                "shopping"
            ],
            "school": [
                "school",
                "education",
                "university",
                "academy",
                "college",
                "teacher",
                "classroom",
                "grammar school"
            ],
            "hospital": [
                "hospital",
                "clinic",
                "outpatient",
                "patient",
                "surgeon",
                "nurse",
                "psychiatric hospital",
                "surgery"
            ],
            "airport": [
                "airport",
                "aerodrome",
                "hangar",
                "runway",
                "airport terminal",
                "landing",
                "heliport",
                "airfield"
            ],
            "stadium": [
                "stadium",
                "arena",
                "baseball",
                "ballpark",
                "dome",
                "park",
                "football",
                "association football"
            ],
            "government": [
                "government",
                "governance",
                "administration",
                "politics",
                "democracy",
                "governing",
                "state",
                "judiciary"
            ],
            "body of water": [
                "body of water",
                "lake",
                "water",
                "ocean",
                "sea",
                "inlet",
                "river",
                "puddle"
            ],
            "mountain": [
                "mountain",
                "hill",
                "volcano",
                "mount",
                "glacier",
                "magma",
                "mount everest",
                "orogeny"
            ],
            "park": [
                "park",
                "playground",
                "recreation",
                "green",
                "ballpark",
                "tract",
                "garden",
                "national park"
            ],
            "island": [
                "island",
                "greenland",
                "continent",
                "australia",
                "borneo",
                "madagascar",
                "singapore",
                "archipelago"
            ],
            "movie": [
                "movie",
                "film",
                "television",
                "movie projector",
                "soundtrack",
                "picture",
                "cinema",
                "dvd"
            ],
            "music": [
                "music",
                "piano",
                "jazz",
                "sound",
                "melody",
                "guitar",
                "song",
                "sheet music"
            ],
            "broadcast": [
                "broadcast",
                "radio",
                "air",
                "television",
                "telecast",
                "circulate",
                "spread",
                "rebroadcast"
            ],
            "video game": [
                "video game",
                "computer game",
                "game",
                "arcade game",
                "electronic game",
                "video game console",
                "xbox one",
                "playstation 4"
            ],
            "war": [
                "war",
                "warfare",
                "battle",
                "conflict",
                "fight",
                "struggle",
                "combat",
                "vietnam war"
            ],
            "disaster": [
                "disaster",
                "catastrophe",
                "calamity",
                "tragedy",
                "tsunami",
                "famine",
                "devastation",
                "earthquake"
            ],
            "competition": [
                "competition",
                "contest",
                "tournament",
                "competitiveness",
                "championship",
                "race",
                "rivalry",
                "sport"
            ],
            "festival": [
                "festival",
                "holiday",
                "celebration",
                "fete",
                "christmas",
                "carnival",
                "gala",
                "jubilee"
            ],
            "language": [
                "language",
                "speech",
                "dialect",
                "word",
                "words",
                "vocabulary",
                "sign language",
                "terminology"
            ],
            "award": [
                "award",
                "prize",
                "trophy",
                "medal",
                "honor",
                "grant",
                "accolade",
                "honour"
            ],
            "disease": [
                "disease",
                "virus",
                "cancer",
                "syndrome",
                "infection",
                "symptom",
                "illness",
                "infectious disease"
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
