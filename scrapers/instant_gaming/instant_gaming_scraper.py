
from selenium import webdriver
from selenium.webdriver import Chrome
from aids import *



def getPageGames(driver: Chrome, games={}):
    pass


def instant_gaming_scrape(search_engine="Edge"):
    link_template = "https://www.instant-gaming.com/es/busquedas/?platform%5B0%5D=1&type%5B0%5D=&sort_by=&min_reviewsavg=10&max_reviewsavg=100&noreviews=1&min_price=0&max_price=200&noprice=1&gametype=games&search_tags=0&query=&page={page}"

    driver = set_driver(search_engine)

    games = {}
    i = 0
    while True:
        driver.get(link_template.format(page=i))
        games = getPageGames(driver, games)
        i += 1