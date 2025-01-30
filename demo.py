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


def metacritic(search_engine="Edge"):
    

    t = start()   #Medir el momento en el que se epieza el scrapping

    games = {}    #Crear diccionario donde se guardan los juegos

    driver = set_driver(search_engine) #Generamos el driver
    driver.implicitly_wait(1)

    #Quitar cookies, no reaparecen
    driver.get(f'https://www.metacritic.com/browse/game/pc/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2025&platform=pc&page=1')
    driver.implicitly_wait(1)
    aceptar = driver.find_element(By.ID,'onetrust-accept-btn-handler')
    pags = 10
    print(pags)
    aceptar.click()

    for i in range(1,int(pags)):

        driver.get(f'https://www.metacritic.com/browse/game/pc/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2025&platform=pc&page={i}')
        games = metacritic_scraper.getPageGames(driver, games)
        print(f'Página hecha {i} de {pags-1} {i/(pags-1)*100:3}%')

    b = finish(t)    #Calculamos el tiempo final
    print("*" * 100, "\n" * 5)

    dump_into(games, "metacriticGamesDemo")    #Insertamos el diccionario games en el json de cdkeys
    print(f"{b} segundos")      #Mostramos el tiempo final
    driver.close()    #Cerramos el driver



def cdkeys(search_engine = "Edge", pags = 10):

    t = start()   #Medir el momento en el que se epieza el scrapping

    games = {}    #Crear diccionario donde se guardan los juegos

    driver = set_driver(search_engine) #Generamos el driver
    driver.implicitly_wait(1)

    

    for i in range(1,pags):

        driver.get(f'https://www.cdkeys.com/es_es/pc/juegos?p={i}')

        games = cdkeys_scraper.getPageGames(driver, games)

        print(f'Página hecha {i} de {pags-1} {i/(pags-1)*100:3}%')       
    
    b = finish(t)    #Calculamos el tiempo final
    print("*" * 100, "\n" * 5)

    dump_into(games, "cdkeysGamesDemo")    #Insertamos el diccionario games en el json de cdkeys
    print(f"{b} segundos")      #Mostramos el tiempo final
    driver.close()    #Cerramos el driver


# funciones que por defecto cambiaban el json real las adaptamos para la demo
def _get_paths_demo() -> list:
    import glob
    paths = []
    for filepath in glob.iglob('*.json'):
        if filepath == '':
            pass
        else:
            paths.append(filepath)
    return paths

def gen_json(sorted=False, dic_games:json_aids.Dict[str, list]=json_aids._merge(_get_paths_demo())):
    with open("games.json", "w+") as outfile:
        if sorted:
            gen_json(False, json_aids.sort(dic_games))
        else:
            json_aids.json.dump(dic_games, outfile)


steam()
cdkeys()
metacritic()


gen_json(True, json_aids._merge(_get_paths_demo()))