
from aids import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome # Ayuda para el autocompletado de funciones en el IDE



def getPageGames(driver: Chrome, games={}):
    elements = driver.find_elements(by=By.CLASS_NAME, value='gASJ2lL_xmVNuZkWGvrWg')
    for element in elements:
        try:
            name = element.find_element(by=By.CSS_SELECTOR, value='._2ekpT6PjwtcFaT4jLQehUK.StoreSaleWidgetTitle').text
            price = element.find_element(by=By.CLASS_NAME, value='_3j4dI1yA7cRfCvK8h406OB').text
            games[name] = (price, "Steam")
        except Exception as e:
            print(f"Error al procesar un elemento: {e}")
    return games


def steam_multiple_scrape(categories=["singleplayer", "multiplayer_mmo", "multiplayer", "multiplayer_local_party", "multiplayer_lan", "multiplayer_coop", "multiplayer_online_competitive"], search_engine="Edge"):
    # Cambia el driver según el navegador que uses
    driver = set_driver(search_engine)

    driver.implicitly_wait(3)
    t = start()
    games = {}

    i = 0
    last_len = 0
    link_template = "https://store.steampowered.com/category/{category}/?offset={offset}"
    for category in categories:
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
                            """)# Baja por la página de forma "smooth" para cargar el contenido de los juegos
                                # Elimina el panel grande de la parte superior de la pantalla (cubría el botón buscar más)

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

    dump_into(games, "steamGames")
    print(f"{b} segundos")


def steam_category_scrape(category: str, search_engine: str):
    # Cambia el driver según el navegador que uses
    driver = set_driver(search_engine)

    driver.implicitly_wait(3)
    t = start()
    games = {}

    i = 0
    last_len = 0
    link_template = "https://store.steampowered.com/category/{category}/?offset={offset}"
    
    last_len = len(games)

    # Para el scrape de "singleplayer", que tiene muchos juegos, merece la pena dividir la tarea en varios procesos paralelos que comiencen en una i distinta.
    '''
    first = int(input("Desde qué i quieres empezar? "))
    i = first
    a = 0
    twelve = True
    while True and i < first + 60000:
    '''

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
    
    dump_into(games, f"steamGames{category}")
    print(f"{b} segundos")

