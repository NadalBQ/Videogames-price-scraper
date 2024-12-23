from aids import *
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Edge()
# driver = webdriver.Chrome()


def getPageGames(driver):
    elements = driver.find_elements(by=By.CLASS_NAME, value='ais-Hits-item')
    games = {}
    for element in elements:
        name = element.find_element(by=By.CLASS_NAME, value='ais-Highlight-nonHighlighted').text
        price = element.find_element(by=By.CLASS_NAME, value='s-hit--price').text
        games[name] = price
    return games

        
def nextPage(driver):
    
    buttons = driver.find_element(by=By.CLASS_NAME, value='s-pagination')
    #print(1, buttons)
    buttons = buttons.find_element(by=By.TAG_NAME, value='div')
    #print(2, buttons)
    buttons = buttons.find_element(by=By.TAG_NAME, value='ul')
    #print(3, buttons)
    buttons = buttons.find_elements(by=By.TAG_NAME, value='li')
    #print(4, buttons)
    button = buttons[-1]
    #print(5, button)
    button.click()

link = "https://steamdb.info/instantsearch/?refinementList%5BappType%5D%5B0%5D=Game"
driver.get(link)
#print("a")
#print(type(driver))

a = start()
games = {}
fails = []
i = -1
more = True
while more:

    i += 1
    #print(i, games)
    try:
        wait(100, "ms")
        page_games = getPageGames(driver)
        
        wait(100, "ms")
        nextPage(driver)
        for name in page_games.keys():
            if games[name] is not None:
                more = False
            games[name] = page_games[name]
        
    except:
        fails.append(i)
        
if fails:
    while len(fails) > 0:
        num = fails.pop()
        try:
            link = f"https://steamdb.info/instantsearch/?page={str(num)}&refinementList%5BappType%5D%5B0%5D=Game"
            driver.get(link)
            wait(10, "ms")
            page_games = getPageGames(driver)
            
            wait(10, "ms")
            nextPage(driver)
            for name in page_games.keys():
                games[name] = page_games[name]

        except:
            fails.append(num)
        if len(fails) == 0:
            break
b = finish(a)
print("*"*100, "\n"*5)
print(games)
print(fails)
print(b, "segundos")

