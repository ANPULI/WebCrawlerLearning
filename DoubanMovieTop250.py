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
    # movie_name_list = []
    movie_dict = {}
    global rank
    for movie_li in movie_list_soup.find_all("li"):
        info = movie_li.find("div", attrs={"class": "hd"})
        movie_name = info.find("span", attrs={"class": "title"}).getText()

        detail = movie_li.find("div", attrs={"class": "bd"})
        star = detail.find("div", attrs={"class": "star"})
        rating_num = star.find("span", attrs={"class": "rating_num"}).getText()

        quote = detail.find("p", attrs={"class": "quote"})
        if quote is None:
            quote_content = None
        else:
            quote_content = quote.find("span", attrs={"class": "inq"}).getText()

        # movie_name_list.append("No." + str(rank) + " " + movie_name + " " + "Rate: " + str(rating_num))
        movie_dict[movie_name] = [rank, rating_num, quote_content]
        rank += 1
    next_page = soup.find("span", attrs={"class": "next"}).find("a")
    if next_page:
        return movie_dict, DOWNLOAD_URL + next_page["href"]
        # return movie_name_list, DOWNLOAD_URL + next_page["href"]
    return movie_dict, None
    # return movie_name_list, None


def main():
    url = DOWNLOAD_URL
    with codecs.open("movies", "wb", encoding="utf-8") as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            # fp.write(u"{movies}\n".format(movies="\n".join(movies)))
            for movie in movies:
                fp.write(u"No.{rank} {movie} Rate: {rating_num}\n\t{quote_content}\n".format(rank=movies[movie][0], movie=movie, rating_num=movies[movie][1], quote_content=movies[movie][2]))
    print("finished!")


if __name__ == "__main__":
    main()


