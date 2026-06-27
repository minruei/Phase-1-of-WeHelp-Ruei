import urllib.request
from bs4 import BeautifulSoup

# 抓一個列表頁，回傳這頁所有文章資料
def parse_article_list(list_url, output_file):
    req = urllib.request.Request(list_url)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    entries = soup.find_all("div", class_="r-ent")

    for entry in entries:
        title_tag = entry.find("a")
        if title_tag is None:
            continue
        title = title_tag.text

        nrec_tag = entry.find("div", class_="nrec")
        if nrec_tag.text == "":
            like_count = "0"
        else:
            like_count = nrec_tag.text

        link = "https://www.ptt.cc" + title_tag["href"]

        article_req = urllib.request.Request(link)
        article_response = urllib.request.urlopen(article_req)
        article_html = article_response.read().decode("utf-8")
        article_soup = BeautifulSoup(article_html, "html.parser")

        meta_values = article_soup.find_all("span", class_="article-meta-value")
        try:
            publish_time = meta_values[3].text
        except:
            publish_time = ""

        output_file.write(title + "," + like_count + "," + publish_time + "\n")


# 找出上頁網址
def get_prev_url(list_url):
    req = urllib.request.Request(list_url)
    response = urllib.request.urlopen(req)
    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # 找有「上頁」字樣的按鈕
    buttons = soup.find_all("a", class_="btn")
    for btn in buttons:
        if "上頁" in btn.text:
            return "https://www.ptt.cc" + btn["href"]
    return None


# ===== 主程式：跑前 3 個列表頁，寫進 articles.csv =====
output_file = open("articles.csv", "w", encoding="utf-8")

list_url = "https://www.ptt.cc/bbs/Steam/index.html"

for page in range(3):
    parse_article_list(list_url, output_file)
    list_url = get_prev_url(list_url)

output_file.close()