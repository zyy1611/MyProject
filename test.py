from openprompt.data_utils import InputExample
from openprompt.prompts import ManualTemplate
from openprompt.prompts import ManualVerbalizer
from openprompt import PromptForClassification
from openprompt import PromptDataLoader
from openprompt.plms import load_plm
import torch
import json

classes = ['athlete', 'musician', 'actor', 'statesman', 'writer', 'leader', 'businessman', 'royal', 'philosopher',
           'country', 'city', 'continent', 'brand', 'software', 'airplane', 'recreation', 'vehicle', 'club',
           'institution', 'sports team', 'political party', 'company', 'government', 'army', 'religion',
           'sports league', 'mall', 'school', 'hospital', 'airport', 'stadium', 'residence', 'body of water', 'island',
           'mountain', 'park', 'movie', 'music', 'painting', 'broadcast', 'war', 'disaster', 'sporting events',
           'festival', 'language', 'law', 'award', 'disease', 'currency']

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
                                    meta={"sentence": json_data[obj]["description"],
                                          "ent": json_data[obj]["ent_name"]}))
        pos = pos + 1
    plm, tokenizer, model_config, WrapperClass = load_plm("bert", "bert-base-uncased")
    promptTemplate = ManualTemplate(
        text='{"meta":"sentence"},In this sentence,{"meta": "ent"} is {"mask"}',
        tokenizer=tokenizer,
    )

    promptVerbalizer = ManualVerbalizer(
        classes=classes,
        label_words={
            "athlete": [
                "athlete",
                "sport",
                "sportsman",
                "skater",
                "jock",
                "swimmer",
                "olympian",
                "gymnast",
                "skier",
                "weightlifter"
            ],
            "musician": [
                "musician",
                "music",
                "composer",
                "pianist",
                "bassist",
                "singer",
                "percussionist",
                "violinist",
                "flutist",
                "instrumentalist"
            ],
            "actor": [
                "actor",
                "comedy",
                "barrymore",
                "mime",
                "actress",
                "drama",
                "thespian",
                "doer",
                "fairbanks",
                "performer"
            ],
            "statesman": [
                "statesman",
                "politician",
                "stateswoman",
                "solon",
                "national leader",
                "politico",
                "elder statesman",
                "georges clemenceau",
                "mikhail sergeyevich gorbachev"
            ],
            "writer": [
                "writer",
                "author",
                "poet",
                "essayist",
                "novelist",
                "bronte",
                "burroughs",
                "literature",
                "scriptwriter",
                "journalist"
            ],
            "leader": [
                "leader",
                "chief",
                "chieftain",
                "politician",
                "goal",
                "leadership",
                "head",
                "commander",
                "lawmaker",
                "guru"
            ],
            "businessman": [
                "businessman",
                "entrepreneur",
                "merchant",
                "business",
                "businessperson",
                "tycoon",
                "industrialist",
                "magnate",
                "owner",
                "oilman"
            ],
            "royal": [
                "royal",
                "imperial",
                "noble",
                "king",
                "regal",
                "queen",
                "monarch",
                "prince",
                "princess",
                "coronation"
            ],
            "philosopher": [
                "philosopher",
                "philosophy",
                "aristotle",
                "immanuel kant",
                "scholar",
                "pythagoras",
                "nietzsche",
                "naturalist",
                "plato",
                "theology"
            ],
            "country": [
                "country",
                "nation",
                "state",
                "land",
                "fatherland",
                "malta",
                "homeland",
                "region",
                "united nations",
                "quadrant"
            ],
            "city": [
                "city",
                "metropolis",
                "town",
                "municipality",
                "urban",
                "suburb",
                "municipal",
                "megalopolis",
                "civilization",
                "village"
            ],
            "continent": [
                "continent",
                "europe",
                "africa",
                "asia",
                "antarctica",
                "oceania",
                "australia",
                "north america",
                "south america",
                "australasia"
            ],
            "brand": [
                "brand",
                "mark",
                "label",
                "trademark",
                "advertising",
                "logo",
                "marketing",
                "blade",
                "trade name",
                "stigmatize"
            ],
            "software": [
                "software",
                "computer program",
                "linux",
                "compiler",
                "data",
                "computer science",
                "program",
                "malware",
                "hardware",
                "computing"
            ],
            "airplane": [
                "airplane",
                "plane",
                "airliner",
                "propeller",
                "monoplane",
                "fuselage",
                "jet",
                "biplane",
                "aeroplane",
                "aircraft"
            ],
            "recreation": [
                "recreation",
                "play",
                "amusement",
                "fun",
                "diversion",
                "leisure",
                "pastime",
                "game",
                "entertainment",
                "park"
            ],
            "vehicle": [
                "vehicle",
                "bicycle",
                "motorcycle",
                "wheel",
                "truck",
                "car",
                "bus",
                "automobile",
                "aircraft",
                "wagon"
            ],
            "club": [
                "club",
                "bludgeon",
                "golf club",
                "nightclub",
                "cudgel",
                "truncheon",
                "baton",
                "gather",
                "clubhouse",
                "lodge"
            ],
            "institution": [
                "institution",
                "establishment",
                "organization",
                "founding",
                "academy",
                "foundation",
                "creation",
                "university",
                "academic",
                "society"
            ],
            "sports team": [
                "sports team",
                "team",
                "sport",
                "lacrosse"
            ],
            "political party": [
                "political party",
                "conservative party",
                "republican party",
                "democracy",
                "democratic party",
                "party",
                "kuomintang",
                "third party",
                "opposition",
                "liberal party"
            ],
            "company": [
                "company",
                "business",
                "corporation",
                "subsidiary",
                "companion",
                "troupe",
                "accompany",
                "unit",
                "fellowship",
                "distributor"
            ],
            "government": [
                "government",
                "governance",
                "administration",
                "politics",
                "democracy",
                "governing",
                "state",
                "judiciary",
                "political science",
                "authorities"
            ],
            "army": [
                "army",
                "military",
                "soldier",
                "militia",
                "conscription",
                "infantry",
                "war machine",
                "regular army",
                "air force",
                "armed forces"
            ],
            "religion": [
                "religion",
                "buddhism",
                "judaism",
                "faith",
                "christianity",
                "islam",
                "hinduism",
                "cult",
                "belief",
                "sikhism"
            ],
            "sports league": [
                "sports league",
                "tournament",
                "association football",
                "conference"
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
                "grammar school",
                "student",
                "primary school"
            ],
            "hospital": [
                "hospital",
                "clinic",
                "outpatient",
                "patient",
                "surgeon",
                "nurse",
                "psychiatric hospital",
                "surgery",
                "physician",
                "infirmary"
            ],
            "airport": [
                "airport",
                "aerodrome",
                "hangar",
                "runway",
                "airport terminal",
                "landing",
                "heliport",
                "airfield",
                "taxiway",
                "control tower"
            ],
            "stadium": [
                "stadium",
                "arena",
                "baseball",
                "ballpark",
                "dome",
                "park",
                "football",
                "association football",
                "coliseum",
                "sport"
            ],
            "residence": [
                "residence",
                "hall",
                "home",
                "house",
                "palace",
                "manse",
                "mansion",
                "apartment",
                "bedroom",
                "domicile"
            ],
            "body of water": [
                "body of water",
                "lake",
                "water",
                "ocean",
                "sea",
                "inlet",
                "river",
                "puddle",
                "stream",
                "waterfall"
            ],
            "island": [
                "island",
                "greenland",
                "continent",
                "australia",
                "borneo",
                "madagascar",
                "singapore",
                "archipelago",
                "mainland",
                "iceland"
            ],
            "mountain": [
                "mountain",
                "hill",
                "volcano",
                "mount",
                "glacier",
                "magma",
                "mount everest",
                "orogeny",
                "mountainside",
                "river"
            ],
            "park": [
                "park",
                "playground",
                "recreation",
                "green",
                "ballpark",
                "tract",
                "garden",
                "national park",
                "stadium",
                "grass"
            ],
            "movie": [
                "movie",
                "film",
                "television",
                "movie projector",
                "soundtrack",
                "picture",
                "cinema",
                "dvd",
                "movie theater",
                "celluloid"
            ],
            "music": [
                "music",
                "piano",
                "jazz",
                "sound",
                "melody",
                "guitar",
                "song",
                "sheet music",
                "classical music",
                "rhythm"
            ],
            "painting": [
                "painting",
                "pigment",
                "oil paint",
                "acrylic paint",
                "repaint",
                "stipple",
                "acrylic",
                "watercolor",
                "watercolour",
                "latex"
            ],
            "broadcast": [
                "broadcast",
                "radio",
                "air",
                "television",
                "telecast",
                "circulate",
                "spread",
                "rebroadcast",
                "simulcast",
                "publicize"
            ],
            "war": [
                "war",
                "warfare",
                "battle",
                "conflict",
                "fight",
                "struggle",
                "combat",
                "vietnam war",
                "genocide",
                "state of war"
            ],
            "disaster": [
                "disaster",
                "catastrophe",
                "calamity",
                "tragedy",
                "tsunami",
                "famine",
                "devastation",
                "earthquake",
                "hardship",
                "cataclysm"
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
                "jubilee",
                "event",
                "oktoberfest"
            ],
            "language": [
                "language",
                "speech",
                "dialect",
                "word",
                "words",
                "vocabulary",
                "sign language",
                "terminology",
                "syntax",
                "linguistics"
            ],
            "law": [
                "law",
                "jurisprudence",
                "constitution",
                "state",
                "canon law",
                "civil law",
                "common law",
                "statute",
                "natural law",
                "rule"
            ],
            "award": [
                "award",
                "prize",
                "trophy",
                "medal",
                "honor",
                "grant",
                "accolade",
                "honour",
                "nobel prize",
                "excellence"
            ],
            "disease": [
                "disease",
                "virus",
                "cancer",
                "syndrome",
                "infection",
                "symptom",
                "illness",
                "infectious disease",
                "malaria",
                "leprosy"
            ],
            "currency": [
                "currency",
                "money",
                "dollar",
                "banknote",
                "coin",
                "legal tender",
                "franc",
                "medium of exchange",
                "paper money",
                "cash"
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
