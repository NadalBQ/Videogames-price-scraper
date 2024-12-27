import json
from aids import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome

# Cambia el driver según el navegador que uses
driver = webdriver.Edge()
# driver = webdriver.Chrome()
driver.implicitly_wait(3)

categories = ["singleplayer", "multiplayer_mmo", "multiplayer", "multiplayer_local_party", "multiplayer_lan", "multiplayer_coop", "multiplayer_online_competitive"]


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

def mostrarMas(driver: Chrome):
    driver.execute_script("""scrollBy({top:10000000000000000, left:0, behavior: "smooth"});
                          let elem = document
                          .querySelector("._1cOoCFwafBlSkwllIMf3XM._1FPIVJTLsw1nvAN24BGGKg.SaleSectionTabs");
                          
                          if (elem) {
                          elem.remove();
                          }
                          """)

    div = driver.find_element(by=By.CLASS_NAME, value='_36qA-3ePJIusV1oKLQep-w')
    button = div.find_element(by=By.CSS_SELECTOR, value='._2tkiJ4VfEdI9kq1agjZyNz.Focusable')

    # Scroll to the button
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    wait(2)
    if button.is_displayed() and button.is_enabled():
        
        button.click()
        driver.execute_script("""scrollBy({top:-10000000000000000, left:0, behavior: "smooth"});""")
        wait(2)  # Esperar un poco para cargar más elementos
    else:
        print("Botón 'Mostrar más' no disponible.")
    

a = start()
games = {}

i = 0
last_len = 0
link_template = "https://store.steampowered.com/category/{category}/?offset={offset}"
for category in categories:
    lastest_len = last_len
    last_len = len(games)
    while True:

        driver.get(link_template.format(category=category, offset=i))
        i += 12
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
        print(len(games))
        if last_len == len(games) and lastest_len == last_len:
            break
        lastest_len = last_len
        last_len = len(games)

b = finish(a)
print("*" * 100, "\n" * 5)
# print(games)
print(f"{b} segundos")


with open("steamGames.json", "w+") as outfile:
    json.dump(games, outfile)
