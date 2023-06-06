from bs4 import BeautifulSoup
import requests
import json

class WebScrapper():
    def __init__(self, link: str) -> None:
        self.link = link
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
        self.get_data()

    def get_data(self) -> None:
        page = requests.get(self.link, headers=self.headers)
        getpage_soup= BeautifulSoup(page.text, 'html.parser')
        data_object = getpage_soup.findAll('script', {'id':'__NEXT_DATA__'})[0]
        self.json_data = json.loads(str(data_object)[51:-9])

    def get_tconst(self) -> str:
        return self.json_data["props"]["pageProps"]["tconst"]
    
    def get_titleType(self) -> str:
        return self.json_data["props"]["pageProps"]["aboveTheFoldData"]["titleType"]["id"]

    def get_primaryTitle(self) -> str:
        return self.json_data["props"]["pageProps"]["aboveTheFoldData"]["titleText"]["text"]

    def get_originalTitle(self) -> str:
        return self.json_data["props"]["pageProps"]["aboveTheFoldData"]["originalTitleText"]["text"]

    def get_isAdult(self) -> bool:
        return self.json_data["props"]["pageProps"]["mainColumnData"]["isAdult"]

    def get_startYear(self) -> str:
        return self.json_data["props"]["pageProps"]["aboveTheFoldData"]["releaseYear"]["year"]

    def get_endYear(self) -> str:
        return self.json_data["props"]["pageProps"]["aboveTheFoldData"]["releaseYear"]["endYear"]

    def get_runtimeMinutes(self) -> int:
        return int(self.json_data["props"]["pageProps"]["aboveTheFoldData"]["runtime"]["seconds"] / 60)

    def get_genres(self) -> list:
        genres = []
        for genre in self.json_data["props"]["pageProps"]["aboveTheFoldData"]["genres"]["genres"]:
            genres.append(genre['id'])

        return genres
    
    def __dict__(self) -> dict:
        return {
            "tconst": self.get_tconst(),
            "titleType": self.get_titleType(),
            "primaryTitle": self.get_primaryTitle(),
            "originalTitle": self.get_originalTitle(),
            "isAdult": self.get_isAdult(),
            "startYear": self.get_startYear(),
            "endYear": self.get_endYear(),
            "runtimeMinutes": self.get_runtimeMinutes(),
            "genres": self.get_genres()
        }

        


if __name__ == "__main__":
    test = WebScrapper("https://www.imdb.com/title/tt0000001")
    # print(test.get_tconst())
    # print(test.get_titleType())
    # print(test.get_primaryTitle())
    # print(test.get_originalTitle())
    # print(test.get_isAdult())
    # print(test.get_startYear())
    # print(test.get_endYear())
    # print(test.get_runtimeMinutes())
    # print(test.get_genres())
    print(test.__dict__())