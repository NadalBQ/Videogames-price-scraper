from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from scrapers.aids import wait, set_driver, scroll, start, finish, dump_into


def cdkeys_scraper(pags = 537):
    t = start()   #Medir el momento en el que se epieza el scrapping

    games = {}    #Crear diccionario donde se guardan los juegos

    for i in range(1,pags):

        driver.get(f'https://www.cdkeys.com/es_es/pc/juegos?p={i}')

        for juego in driver.find_elements(By.CLASS_NAME,'product-item '):
            lista = juego.text.split('\n')
            if len(lista)==4:
                games[lista[1]] = lista[2]
            elif len(lista)==5:
                games[lista[2]] = lista[3]
        print(f'Página hecha {i} de {pags-1} {i/(pags-1)*100:3}%')

    b = finish(t)    #Calculamos el tiempo final
    print("*" * 100, "\n" * 5)

    dump_into(games, "jsons/cdkeysGames")    #Insertamos el diccionario games en el json de cdkeys
    print(f"{b} segundos")      #Mostramos el tiempo final