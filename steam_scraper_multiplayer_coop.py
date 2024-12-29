from steam_scraper import getPageGames
from aids import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome

# Cambia el driver según el navegador que uses
driver = webdriver.Edge()
# driver = webdriver.Chrome()
driver.implicitly_wait(3)

categories = ["multiplayer_coop"]
   

t = start()
games = {}

i = 0
last_len = 0
link_template = "https://store.steampowered.com/category/{category}/?offset={offset}"
for category in categories:
    lastest_len = last_len
    last_len = len(games)
    i = 0
    a = 0
    twelve = True
    while True:

        driver.get(link_template.format(category=category, offset=i))
        # i += 12
        wait(100, "ms")
        driver.execute_script("""scrollBy({top:10000000000000000, left:0, behavior: "smooth"});
                          let elem = document
                          .querySelector("._1cOoCFwafBlSkwllIMf3XM._1FPIVJTLsw1nvAN24BGGKg.SaleSectionTabs");
                          
                          if (elem) {
                          elem.remove();
                          }
                          """)

        print("gettin games!")
        games = getPageGames(driver, games)
        print("games:", len(games), "a:", a, "i:", i)
        if len(games) != last_len:
            a = 0
        if a == 0:
            twelve = True
        else:
            twelve = False
        
        if twelve:
            i += 12
        else:
            i += 1

        if a > 144:
            break
        elif last_len == len(games):
            a += 1
        last_len = len(games)

b = finish(t)
print("*" * 100, "\n" * 5)
# print(games)
print(f"{b} segundos")


dump_into(games, f"steamGamesMultiplayerCOOP{str(i)}")
