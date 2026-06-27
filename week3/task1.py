import urllib.request
import json
import csv
import re

def fetch_json(url):
    with urllib.request.urlopen(url) as resp:
        text = resp.read().decode('utf-8')
        return json.loads(text)

CH_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
EN_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

ch_data = fetch_json(CH_URL)
en_data = fetch_json(EN_URL)

# 建立英文對照表: key 是 _id,value 是英文資料
en_lookup = {}
for hotel in en_data["list"]:
    en_lookup[hotel["_id"]] = hotel

# 合併，把每間中文旅館對應英文資料
hotels = []
for ch in ch_data["list"]:
    hotel_id = ch["_id"]
    en = en_lookup[hotel_id]   # 用 _id 查對應英文資料

    hotels.append({
        "ChineseName":      ch["旅宿名稱"],
        "EnglishName":      en["hotel name"],
        "ChineseAddress":   ch["地址"],
        "EnglishAddress":   en["address"],
        "Phone":            ch["電話或手機號碼"],
        "RoomCount":        ch["房間數"],
    })

# 寫進 hotels.csv
with open("hotels.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for h in hotels:
        writer.writerow([
            h["ChineseName"],
            h["EnglishName"],
            h["ChineseAddress"],
            h["EnglishAddress"],
            h["Phone"],
            h["RoomCount"],
        ])

# 從地址抓出區，例如 臺北市萬華區... → 萬華區
def get_district(address):
    match = re.search(r"市(.+?區)", address)
    if match:
        return match.group(1)
    return ""

# 統計各區的旅館數和房間數
districts = {}
for h in hotels:
    d = get_district(h["ChineseAddress"])
    if d == "":
        continue   # 抓不到就跳過

    if d not in districts:
        districts[d] = {"hotels": 0, "rooms": 0}   # 建空櫃位

    districts[d]["hotels"] += 1                     # 這區旅館數 +1
    districts[d]["rooms"] += int(h["RoomCount"])    # 房間數累加，int 轉數字

# 寫進 districts.csv
with open("districts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for d in districts:
        writer.writerow([d, districts[d]["hotels"], districts[d]["rooms"]])

print("完成！hotels.csv 和 districts.csv 都寫好了!")