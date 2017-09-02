import requests
from bs4 import BeautifulSoup

# init the url
url = "http://news.qq.com/"
# request Tecent news and get its text
wbdata = requests.get(url).text
# analyze the text we get
soup = BeautifulSoup(wbdata, "html.parser")
# using select to locate the element and return a list
news_titles = soup.select("div.text > em.f14 > a.linkto")

# go through the list
for news_title in news_titles:
    # get title and link
    title = news_title.get_text()
    link = news_title.get("href")
    data = {
        "title": title,
        "link": link
    }
    print(data)