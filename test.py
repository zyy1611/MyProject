from openprompt.data_utils import InputExample
from openprompt.prompts import ManualTemplate
from openprompt.prompts import ManualVerbalizer
from openprompt import PromptForClassification
from openprompt import PromptDataLoader
from openprompt.plms import load_plm
import torch
import json

classes = ['sportsman', 'singer', 'performer', 'leader', 'businessman', 'royal', 'philosopher', 'country', 'city',
           'brand', 'airplane', 'vehicle', 'club', 'sports team', 'company', 'government', 'army', 'religion',
           'politics', 'mall', 'university', 'hospital', 'airport', 'stadium', 'body of water', 'island', 'mountain',
           'park', 'movie', 'song', 'broadcast', 'video game', 'war', 'disaster', 'sporting events', 'festival',
           'language', 'award', 'disease', 'currency']

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
        dataset.append(InputExample(guid=0, label=int(obj),
                                    meta={"sentence": json_data[obj]["description"].replace(json_data[obj]["ent_name"],
                                                                                            "entity"),
                                          "ent": "entity"}))
        pos = pos + 1
    plm, tokenizer, model_config, WrapperClass = load_plm("bert", "bert-base-uncased")
    promptTemplate = ManualTemplate(
        text='{"meta":"sentence"}.The type of {"meta": "ent"} is {"mask"}',
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
                "jazz"
            ],
            "performer": [
                "performer",
                "actor",
                "dance",
                "dancer",
                "musician",
                "comedian",
                "entertainer",
                "artiste"
            ],
            "leader": [
                "leader",
                "chief",
                "chieftain",
                "politician",
                "goal",
                "leadership",
                "head",
                "commander"
            ],
            "businessman": [
                "businessman",
                "entrepreneur",
                "merchant",
                "business",
                "businessperson",
                "tycoon",
                "industrialist",
                "magnate"
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
            "philosopher": [
                "philosopher",
                "philosophy",
                "aristotle",
                "immanuel kant",
                "scholar",
                "pythagoras",
                "nietzsche",
                "naturalist"
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
            "vehicle": [
                "vehicle",
                "bicycle",
                "motorcycle",
                "wheel",
                "truck",
                "car",
                "bus",
                "automobile"
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
            "religion": [
                "religion",
                "buddhism",
                "judaism",
                "faith",
                "christianity",
                "islam",
                "hinduism",
                "cult"
            ],
            "politics": [
                "politics",
                "government",
                "diplomatic",
                "law",
                "political science",
                "aristotle",
                "politics",
                "diplomatical"
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
            "university": [
                "university",
                "college",
                "educational institution",
                "academia",
                "campus",
                "stanford",
                "harvard",
                "sorbonne"
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
            "song": [
                "song",
                "ballad",
                "lullaby",
                "folk song",
                "aria",
                "music",
                "melody",
                "lyric"
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
            "sporting events": [
                "sporting events",
                "association football",
                "rugby union"
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
            ],
            "currency": [
                "currency",
                "money",
                "dollar",
                "banknote",
                "coin",
                "legal tender",
                "franc",
                "medium of exchange"
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
