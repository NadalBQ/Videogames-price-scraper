
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from scrapers.aids import wait, set_driver, scroll, start, finish, dump_into



def getPageGames(driver: Chrome, games={}):
    try:
        elements = driver.find_elements(by=By.CSS_SELECTOR, value='.pFaGHa.WpvaUk')
    except:
        return games, 0
    a = 0
    for element in elements:
        try:
            name = element.find_element(by=By.CLASS_NAME, value='YLosEL').text
            a = 1
            price = element.find_element(by=By.CLASS_NAME, value='L5ErLT').text
            games[name] = (price, "Eneba")
        except Exception as e:
            print(f"Error al procesar un elemento: {e}")
    return games, a


def robot_checker(driver: Chrome): #can't click the checkbox
    cell = driver.find_element(by=By.CSS_SELECTOR, value="class=\"cb-i\"")
    cell.click()
    wait(2)


def eneba_scrape(search_engine="Edge"):
    link_template = "https://www.eneba.com/es/store/games?page={page}"

    driver = set_driver(search_engine)
    driver.implicitly_wait(2)

    t = start()

    games = {}
    i = 1
    fails = 0

    while not bool(len(games) == last_len and a == 0 and fails > 10):
        try:
            last_len = len(games)
            driver.get(link_template.format(page=i))
            
            scroll(driver)
            wait(1)

            games, a = getPageGames(driver, games)
            print("games:", len(games), "fails:", fails, "i:", i)
            
            if len(games) != last_len:
                fails = 0
            if len(games) == last_len and a == 0:
                fails += 1
                wait(2)
                # robot_checker(driver)
            else:
                i += 1
        except:
            print("crash", i)
            break
            
    
    b = finish(t)
    print("*" * 100, "\n" * 5)

    dump_into(games, "jsons/enebaGames")
    print(f"{b} segundos")

