
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from scrapers.aids import wait, set_driver,massive_scroll, start, finish, dump_into



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


def steam_multiple_scrape(search_engine="Edge", categories=["singleplayer", "multiplayer_mmo", "multiplayer", "multiplayer_local_party", "multiplayer_lan", "multiplayer_coop", "multiplayer_online_competitive"]):
    # Cambia el driver según el navegador que uses
    link_template = "https://store.steampowered.com/category/{category}/?offset={offset}"

    driver = set_driver(search_engine)
    driver.implicitly_wait(3)

    t = start()

    games = {}
    i = 0
    last_len = 0
    for category in categories:
        last_len = len(games)
        i = 0 # página a la que hacer scraping
        a = 0 # número de fallos seguidos durante el scraping (un número elevado indicará que hemos visto todo el contenido y no encuentra más)
        twelve = True #aumentar en 12 la i en la búsqueda de juegos
        while a < 145:

            driver.get(link_template.format(category=category, offset=i))
            # i += 12
            wait(100, "ms")
            massive_scroll(driver)
            #driver.execute_script("""scrollBy({top:10000000000000000, left:0, behavior: "smooth"}); let elem = document.querySelector("._1cOoCFwafBlSkwllIMf3XM._1FPIVJTLsw1nvAN24BGGKg.SaleSectionTabs"); if (elem) {elem.remove();}""")
            # Baja por la página de forma "smooth" para cargar el contenido de los juegos
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

            
            if last_len == len(games):
                a += 1
            last_len = len(games)

    b = finish(t)
    print("*" * 100, "\n" * 5)

    dump_into(games, "jsons/steamGames")
    print(f"{b} segundos")


def steam_category_scrape(search_engine="Edge", category="singleplayer"):
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
    while a < 145:

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

        
        if last_len == len(games):
            a += 1
        last_len = len(games)

    b = finish(t)
    print("*" * 100, "\n" * 5)
    
    dump_into(games, f"jsons/steamGames{category}")
    print(f"{b} segundos")

