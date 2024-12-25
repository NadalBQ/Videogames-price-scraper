from aids import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome

# Cambia el driver según el navegador que uses
driver = webdriver.Edge()
# driver = webdriver.Chrome()
driver.implicitly_wait(10)

categories = ["singleplayer", "singleplayer", "multiplayer_mmo", "multiplayer", "multiplayer_local_party", "multiplayer_lan", "multiplayer_coop", "multiplayer_online_competitive"]

def scroll(driver: Chrome):
    SCROLL_PAUSE_TIME = 0.2
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page
        wait(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

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
        button_position = button.location
        button.click()
        driver.execute_script("""scrollBy({top:-10000000000000000, left:0, behavior: "smooth"});""")
        wait(2)  # Esperar un poco para cargar más elementos
    else:
        print("Botón 'Mostrar más' no disponible.")
    

dic_videojuegos = {"jurasic Part": [[(15, "Epic"), (16, "Steam")], 8.5, 40]}

# Inicio del proceso
a = start()
games = {}

i = 0
for category in categories:
    link = f"https://store.steampowered.com/category/{category}/"
    driver.get(link)
    wait(10)
    
    while True:
        i += 1
        try:
            n = start()
            mostrarMas(driver)
            m = finish(n)
            print(f"{int(m)} seconds to click button at {category}")
            
            print(f"Mostrar más {category}, intento {i}")
        except Exception as e:
            print(e)
            input()
            print("Saltando a la siguiente categoría")
            break
    print("gettin games!")
    games = getPageGames(driver, games)

b = finish(a)
print("*" * 100, "\n" * 5)
print(games)
print(f"{b} segundos")
