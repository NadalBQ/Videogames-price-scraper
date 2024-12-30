
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from aids import *



def getPageGames(driver: Chrome, games={}):
    elements = driver.find_elements(by=By.CSS_SELECTOR, value='.item.force-badge')
    for element in elements:
        try:
            name = element.find_element(by=By.CLASS_NAME, value='title').text
            price = element.find_element(by=By.CSS_SELECTOR, value='.price').text
            games[name] = (price, "Instant-Gaming")
        except Exception as e:
            print(f"Error al procesar un elemento: {e}")
    return games


def instant_gaming_scrape(search_engine="Edge"):
    link_template = "https://www.instant-gaming.com/es/busquedas/?platform%5B0%5D=1&type%5B0%5D=&sort_by=&min_reviewsavg=10&max_reviewsavg=100&noreviews=1&min_price=0&max_price=200&noprice=1&gametype=games&search_tags=0&query=&page={page}"

    driver = set_driver(search_engine)
    driver.implicitly_wait(3)

    t = start()

    games = {}
    i = 1
    while True:
        last_len = len(games)
        driver.get(link_template.format(page=i))
        games = getPageGames(driver, games)
        print("games:", len(games), "i:", i)
        

        if len(games) == last_len:
            break
        else:
            i += 1
    
    b = finish(t)
    print("*" * 100, "\n" * 5)

    dump_into(games, "jsons/instantGamingGames")
    print(f"{b} segundos")

instant_gaming_scrape()