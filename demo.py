import scrapers.instant_gaming_scraper as instant_gaming_scraper
import scrapers.steam_scraper as steam_scraper
import scrapers.eneba_scraper as eneba_scraper
import scrapers.cdkeys_scraper as cdkeys_scraper
import scrapers.metacritic_scraper as metacritic_scraper
import jsons.json_aids as json_aids

from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from scrapers.aids import wait, set_driver,massive_scroll, start, finish, dump_into


# Adaptamos la última función del steam_scraper para hacer la búsqueda en pocas páginas

def steam(search_engine:str = "Edge", category:str = "singleplayer"):
    driver = set_driver(search_engine)

    driver.implicitly_wait(3)
    t = start()
    games = {}

    link_template = "https://store.steampowered.com/category/{category}/?offset={offset}"
    
    last_len = len(games)
    first = int(input("Desde qué i quieres empezar? "))
    i = first
    a = 0
    twelve = True
    while i < first + 25:
    
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
        games = steam_scraper.getPageGames(driver, games)
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

        
        if last_len == len(games):
            a += 1
        last_len = len(games)

    b = finish(t)
    print("*" * 100, "\n" * 5)
    
    dump_into(games, f"demo_steam_{category}")
    print(f"{b} segundos")

# funciones que por defecto cambiaban el json real las adaptamos para la demo
def _get_paths_demo() -> list:
    import glob
    paths = []
    for filepath in glob.iglob('*.json'):
        if filepath == 'jsons/games.json' or filepath == 'jsons\\games.json' or filepath == 'jsons\\metacriticGames.json' or filepath == 'jsons/metacriticGames.json':
            pass
        else:
            paths.append(filepath)
    return paths

def gen_json(sorted=False, dic_games:json_aids.Dict[str, list]=json_aids._merge(_get_paths_demo)):
    with open("games.json", "w+") as outfile:
        if sorted:
            gen_json(False, json_aids.sort(dic_games))
        else:
            json_aids.json.dump(dic_games, outfile)










gen_json(True, json_aids._merge(_get_paths_demo()))