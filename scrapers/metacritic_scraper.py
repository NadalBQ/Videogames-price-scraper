from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from scrapers.aids import wait, set_driver, scroll, start, finish, dump_into

def getPageGames(driver: Chrome, games={}):
    for juego in driver.find_elements(By.CLASS_NAME,'c-finderProductCard.c-finderProductCard-game'):
        lista = juego.text.split('\n')
        try:
            titulo = lista[0].split('. ')[1]
        except:
            titulo = 'No cargado.'
        fecha= lista[1]
        Descripción = lista[2]
        try:
            Puntuación = lista[3]
        except:
            Puntuación = 0
        games[titulo]= (fecha,Descripción,Puntuación)
    return games
        
    
def metacritic_scrape(search_engine = "Edge"):

    t = start()   #Medir el momento en el que se epieza el scrapping

    games = {}    #Crear diccionario donde se guardan los juegos

    driver = set_driver(search_engine) #Generamos el driver
    driver.implicitly_wait(1)

    #Quitar cookies, no reaparecen
    driver.get(f'https://www.metacritic.com/browse/game/pc/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2025&platform=pc&page=1')
    driver.implicitly_wait(1)
    aceptar = driver.find_element(By.ID,'onetrust-accept-btn-handler')
    pags = driver.find_element(By.CLASS_NAME,'c-navigationPagination_pages.u-flexbox.u-flexbox-alignCenter.u-flexbox-justifyCenter').text.split('\n')[3]
    pags = int(pags)
    print(pags)
    aceptar.click()

    for i in range(1,int(pags)):

        driver.get(f'https://www.metacritic.com/browse/game/pc/all/all-time/metascore/?releaseYearMin=1958&releaseYearMax=2025&platform=pc&page={i}')
        games = getPageGames(driver, games)
        print(f'Página hecha {i} de {pags-1} {i/(pags-1)*100:3}%')

    b = finish(t)    #Calculamos el tiempo final
    print("*" * 100, "\n" * 5)

    dump_into(games, "jsons/metacriticGames")    #Insertamos el diccionario games en el json de cdkeys
    print(f"{b} segundos")      #Mostramos el tiempo final
    driver.close()    #Cerramos el driver
