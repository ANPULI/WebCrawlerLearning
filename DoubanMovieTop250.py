import requests
from bs4 import BeautifulSoup
import codecs

DOWNLOAD_URL = "https://movie.douban.com/top250"
rank = 1


def download_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_list_soup = soup.find("ol", attrs={"class": "grid_view"})
    movie_name_list = []
    global rank
    for movie_li in movie_list_soup.find_all("li"):
        detail = movie_li.find("div", attrs={"class": "hd"})
        movie_name = detail.find("span", attrs={"class": "title"}).getText()
        movie_name_list.append("No." + str(rank) + " " + movie_name)
        rank += 1
    next_page = soup.find("span", attrs={"class": "next"}).find("a")
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page["href"]
    return movie_name_list, None


def main():
    url = DOWNLOAD_URL
    with codecs.open("movies", "wb", encoding="utf-8") as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            # fp.write("\n".join(movies))
            fp.write(u"{movies}\n".format(movies="\n".join(movies)))
    print("finished!")


if __name__ == "__main__":
    main()


