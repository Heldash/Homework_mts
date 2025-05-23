import time

from bs4 import BeautifulSoup
from selenium import webdriver
import re
import csv
from selenium_stealth import stealth

class Kino():
    def __init__(self,title:str,year:str,country:str,director:str,can_view:bool,raiting:float):
        self.title = title
        self.year = year
        self.country = country
        self.raiting = raiting
        self.director = director
        self.can_view = can_view
    def get_dict(self):
        return {"Название":self.title,
                "Год":self.year,
                "Страна":self.country,
                "Режиссер":self.director,
                "Рейтинг":self.raiting,
                "Смотреть онлайн":self.can_view}
    def get_title(self):
        return self.title
    def get_year(self):
        return self.year
    def get_country(self):
        return self.country
    def get_director(self):
        return self.director
    def get_can_view(self):
        return self.can_view
    def __str__(self):
        return f"Название: {self.title}, год: {self.year}, страна: {self.country}, режиссёр:{self.director}, Доступно на кипопоиске:{self.can_view}, рейтинг:{self.raiting}"


import requests

url = "https://www.kinopoisk.ru/lists/movies/top_1000/"
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
options = webdriver.FirefoxOptions()
# options.add_argument("start-maximized")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--headless')
# options.add_argument('--no-sandbox')
driver = webdriver.Firefox(options=options)
# options = webdriver.ChromeOptions()
# options.add_argument("start-maximized")

# options.add_argument("--headless")

# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# driver = webdriver.Chrome(options=options)
# stealth(driver,
#         languages=["en-US", "en"],
#         vendor="Google Inc.",
#         platform="Win32",
#         webgl_vendor="Intel Inc.",
#         renderer="Intel Iris OpenGL Engine",
#         fix_hairline=True,
#         )
# driver.delete_all_cookies()
driver.get(url)
# time.sleep(10)
res = driver.page_source
# driver.get(url)
# print(res)
bs = BeautifulSoup(res, 'lxml')
print(bs)
# print(type(bs))
kino_list = bs.find_all("div",{"data-test-id":"movie-list-item"})
print(kino_list)
itog = []
page = 1
while len(kino_list)>0:
    for cinema in kino_list:
        cinema = BeautifulSoup(str(cinema), 'lxml')
        # print(type(cinema))
        title = cinema.find("span",{"class":"styles_mainTitle__IFQyZ styles_activeMovieTittle__kJdJj"})
        # print(title.text)
        year = cinema.find("span",{"class":"desktop-list-main-info_secondaryText__M_aus"}).text
        try:
            year = re.findall("\d{4}",year)[0]
        except:
            year = -1
        country_director = cinema.find("span",{"class":"desktop-list-main-info_truncatedText__IMQRP"}).text.split("•")
        try:
            country = country_director[0].strip()
        except:
            country = ""
        # print("country: ",country)
        try:
            director = country_director[1].split("Режиссёр: ")[1]
        except:
            director = ""
        # print("Director: ",country_director[1].split("Режиссёр: ")[1])
        view_button = cinema.find("div",{"class":re.compile("styles_onlineButton*?")})
        # print(view_button)
        # print(type(view_button))
        if view_button is not None:
            can_view = True
        else:
            can_view = False

        raiting = cinema.find("span",{"class":re.compile("styles_kinopoiskValue*?")})
        if raiting == None:
            raiting = -1.0
            # print(title)
        else:
            raiting = float(raiting.text)
        kino = Kino(title.text,year,country,director,can_view,raiting)
        itog.append(kino.get_dict())
        print(kino)
    page+=1
    url = f"https://www.kinopoisk.ru/lists/movies/top_1000/?page={page}"
    driver.get(url)
    res = driver.page_source
    # print(res)
    bs = BeautifulSoup(res, 'lxml')
    # print(type(bs))
    kino_list = bs.find_all("div",{"data-test-id":"movie-list-item"})

with open("result.csv",'w', newline='') as csvfile:
    fieldnames = ['Название', 'Год', 'Страна', 'Режиссер',"Рейтинг","Смотреть онлайн"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(itog)
driver.close()