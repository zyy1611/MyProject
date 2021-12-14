from openprompt.data_utils import InputExample
from openprompt.prompts import ManualTemplate
from openprompt.prompts import ManualVerbalizer
from openprompt import PromptForClassification
from openprompt import PromptDataLoader
from openprompt.plms import load_plm
import torch
import json

classes = ['athlete', 'artist', 'actor', 'politician', 'leader', 'businessman', 'royal', 'country', 'city', 'continent',
           'brand', 'software', 'airplane', 'food', 'game', 'vehicle', 'federation', 'institution', 'sports team',
           'political party', 'education', 'company', 'government', 'army', 'religion', 'sports league', 'mall',
           'school', 'hospital', 'airport', 'residence', 'body of water', 'island', 'mountain', 'park', 'movie',
           'music', 'painting', 'broadcast', 'war', 'disaster', 'election', 'sporting events', 'festival', 'language',
           'law', 'award', 'disease', 'currency']

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
        text='{"meta":"sentence"},{"meta": "ent"} is {"mask"}',
        tokenizer=tokenizer,
    )

    promptVerbalizer = ManualVerbalizer(
        classes=classes,
        label_words={
            "athlete": [
                "sport",
                "sportsman",
                "skater",
                "jock",
                "swimmer",
                "olympian",
                "gymnast",
                "skier",
                "weightlifter",
                "hurdler"
            ],
            "artist": [
                "art",
                "painter",
                "illustrator",
                "musician",
                "artwork",
                "sculptor",
                "photographer",
                "sculpture",
                "decorator",
                "visual art"
            ],
            "actor": [
                "comedy",
                "barrymore",
                "mime",
                "actress",
                "drama",
                "thespian",
                "doer",
                "fairbanks",
                "performer",
                "radio"
            ],
            "politician": [
                "politics",
                "leader",
                "governor",
                "democrat",
                "candidate",
                "statesman",
                "legislator",
                "demagogue",
                "campaigner",
                "political"
            ],
            "leader": [
                "chief",
                "chieftain",
                "politician",
                "goal",
                "leadership",
                "head",
                "commander",
                "lawmaker",
                "guru",
                "president"
            ],
            "businessman": [
                "entrepreneur",
                "merchant",
                "business",
                "businessperson",
                "tycoon",
                "industrialist",
                "magnate",
                "owner",
                "oilman",
                "businesswoman"
            ],
            "royal": [
                "imperial",
                "noble",
                "king",
                "regal",
                "queen",
                "monarch",
                "prince",
                "princess",
                "coronation",
                "purple"
            ],
            "country": [
                "nation",
                "state",
                "land",
                "fatherland",
                "malta",
                "homeland",
                "region",
                "united nations",
                "quadrant",
                "corner"
            ],
            "city": [
                "metropolis",
                "town",
                "municipality",
                "urban",
                "suburb",
                "municipal",
                "megalopolis",
                "civilization",
                "village",
                "downtown"
            ],
            "continent": [
                "europe",
                "africa",
                "asia",
                "antarctica",
                "oceania",
                "australia",
                "north america",
                "south america",
                "australasia",
                "landmass"
            ],
            "brand": [
                "mark",
                "label",
                "trademark",
                "advertising",
                "logo",
                "marketing",
                "blade",
                "trade name",
                "stigmatize",
                "hallmark"
            ],
            "software": [
                "computer program",
                "linux",
                "compiler",
                "data",
                "computer science",
                "program",
                "malware",
                "hardware",
                "computing",
                "computer"
            ],
            "airplane": [
                "plane",
                "airliner",
                "propeller",
                "monoplane",
                "fuselage",
                "jet",
                "biplane",
                "aeroplane",
                "aircraft",
                "aviator"
            ],
            "food": [
                "nutrition",
                "rice",
                "nutrient",
                "beef",
                "meat",
                "provender",
                "victuals",
                "cooking",
                "seafood",
                "pabulum"
            ],
            "game": [
                "play",
                "computer game",
                "tennis",
                "baseball",
                "gamey",
                "pitch",
                "competition",
                "party game",
                "pinball",
                "card game"
            ],
            "vehicle": [
                "bicycle",
                "motorcycle",
                "wheel",
                "truck",
                "car",
                "bus",
                "automobile",
                "aircraft",
                "wagon",
                "train"
            ],
            "federation": [
                "confederation",
                "organization",
                "organisation",
                "union",
                "association",
                "committee",
                "constitution",
                "establishment",
                "confederacy",
                "alliance"
            ],
            "institution": [
                "establishment",
                "organization",
                "founding",
                "academy",
                "foundation",
                "creation",
                "university",
                "academic",
                "society",
                "organisation"
            ],
            "sports team": [
                "team",
                "sport",
                "lacrosse",
                "squad"
            ],
            "political party": [
                "conservative party",
                "republican party",
                "democracy",
                "democratic party",
                "party",
                "kuomintang",
                "third party",
                "opposition",
                "liberal party",
                "war party"
            ],
            "education": [
                "teaching",
                "pedagogy",
                "instruction",
                "school",
                "curriculum",
                "learning",
                "college",
                "university",
                "educational activity",
                "didactics"
            ],
            "company": [
                "business",
                "corporation",
                "subsidiary",
                "companion",
                "troupe",
                "accompany",
                "unit",
                "fellowship",
                "distributor",
                "companionship"
            ],
            "government": [
                "governance",
                "administration",
                "politics",
                "democracy",
                "governing",
                "state",
                "judiciary",
                "political science",
                "authorities",
                "regime"
            ],
            "army": [
                "military",
                "soldier",
                "militia",
                "conscription",
                "infantry",
                "war machine",
                "regular army",
                "air force",
                "armed forces",
                "corps"
            ],
            "religion": [
                "buddhism",
                "judaism",
                "faith",
                "christianity",
                "islam",
                "hinduism",
                "cult",
                "belief",
                "sikhism",
                "atheism"
            ],
            "sports league": [
                "tournament",
                "association football",
                "conference",
                "golf"
            ],
            "mall": [
                "shopping mall",
                "plaza",
                "shop",
                "strip mall",
                "center",
                "downtown",
                "shopping",
                "store"
            ],
            "school": [
                "education",
                "university",
                "academy",
                "college",
                "teacher",
                "classroom",
                "grammar school",
                "student",
                "primary school",
                "secondary school"
            ],
            "hospital": [
                "clinic",
                "outpatient",
                "patient",
                "surgeon",
                "nurse",
                "psychiatric hospital",
                "surgery",
                "physician",
                "infirmary",
                "sanatorium"
            ],
            "airport": [
                "aerodrome",
                "hangar",
                "runway",
                "airport terminal",
                "landing",
                "heliport",
                "airfield",
                "taxiway",
                "control tower",
                "hotel"
            ],
            "residence": [
                "hall",
                "home",
                "house",
                "palace",
                "manse",
                "mansion",
                "apartment",
                "bedroom",
                "domicile",
                "address"
            ],
            "body of water": [
                "lake",
                "water",
                "ocean",
                "sea",
                "inlet",
                "river",
                "puddle",
                "stream",
                "waterfall",
                "waterway"
            ],
            "island": [
                "greenland",
                "continent",
                "australia",
                "borneo",
                "madagascar",
                "singapore",
                "archipelago",
                "mainland",
                "iceland",
                "seychelles"
            ],
            "mountain": [
                "hill",
                "volcano",
                "mount",
                "glacier",
                "magma",
                "mount everest",
                "orogeny",
                "mountainside",
                "river",
                "alpine"
            ],
            "park": [
                "playground",
                "recreation",
                "green",
                "ballpark",
                "tract",
                "garden",
                "national park",
                "stadium",
                "grass",
                "yard"
            ],
            "movie": [
                "film",
                "television",
                "movie projector",
                "soundtrack",
                "picture",
                "cinema",
                "dvd",
                "movie theater",
                "celluloid",
                "screenplay"
            ],
            "music": [
                "piano",
                "jazz",
                "sound",
                "melody",
                "guitar",
                "song",
                "sheet music",
                "classical music",
                "rhythm",
                "harmony"
            ],
            "painting": [
                "pigment",
                "oil paint",
                "acrylic paint",
                "repaint",
                "stipple",
                "acrylic",
                "watercolor",
                "watercolour",
                "latex",
                "distemper"
            ],
            "broadcast": [
                "radio",
                "air",
                "television",
                "telecast",
                "circulate",
                "spread",
                "rebroadcast",
                "simulcast",
                "publicize",
                "cable television"
            ],
            "war": [
                "warfare",
                "battle",
                "conflict",
                "fight",
                "struggle",
                "combat",
                "vietnam war",
                "genocide",
                "state of war",
                "civil war"
            ],
            "disaster": [
                "catastrophe",
                "calamity",
                "tragedy",
                "tsunami",
                "famine",
                "devastation",
                "earthquake",
                "hardship",
                "cataclysm",
                "hurricane"
            ],
            "election": [
                "vote",
                "reelection",
                "legislature",
                "referendum",
                "ballot",
                "poll",
                "electoral",
                "absentee ballot",
                "general election",
                "elect"
            ],
            "sporting events": [
                "association football",
                "rugby union",
                "olympic games"
            ],
            "festival": [
                "holiday",
                "celebration",
                "fete",
                "christmas",
                "carnival",
                "gala",
                "jubilee",
                "event",
                "oktoberfest",
                "fiesta"
            ],
            "language": [
                "speech",
                "dialect",
                "word",
                "words",
                "vocabulary",
                "sign language",
                "terminology",
                "syntax",
                "linguistics",
                "natural language"
            ],
            "law": [
                "jurisprudence",
                "constitution",
                "state",
                "canon law",
                "civil law",
                "common law",
                "statute",
                "natural law",
                "rule",
                "legislation"
            ],
            "award": [
                "prize",
                "trophy",
                "medal",
                "honor",
                "grant",
                "accolade",
                "honour",
                "nobel prize",
                "excellence",
                "emmy"
            ],
            "disease": [
                "virus",
                "cancer",
                "syndrome",
                "infection",
                "symptom",
                "illness",
                "infectious disease",
                "malaria",
                "leprosy",
                "malignancy"
            ],
            "currency": [
                "money",
                "dollar",
                "banknote",
                "coin",
                "legal tender",
                "franc",
                "medium of exchange",
                "paper money",
                "cash",
                "euro"
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
    failed_ids = {"1":[],"2":[]}
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
