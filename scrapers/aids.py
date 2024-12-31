import time
import json
from selenium import webdriver
from selenium.webdriver import Chrome
from typing import Literal


def wait(amount: int, unit="s"):
    """
    Makes the script stop for the time given before taking on the next instruction
    unit types: m, s, ms
    """
    if unit == "s":
        time.sleep(amount)
    elif unit == "m":
        time.sleep(amount*60)
    else:
        time.sleep(amount/1000)


def start():
    return time.time()


def finish(start):
    return time.time() - start


def dump_into(what, where):
    '''
    what: The things you want to put into a json file.
    where: the route name of the file eg. steamGamesSingleplayer.

    This function returns nothing.
    '''
    
    with open(f"{where}.json", "w+") as outfile:
        json.dump(what, outfile)


def set_driver(search_engine: Literal["Chrome", "Safari", "Firefox", "Edge", "Explorer"]="Chrome") -> Chrome:
    '''
    search_engine must be Chrome, Edge or any search engine supported by selenium
    This function returns a webdriver
    '''
    search_engines = ["Chrome", "Safari", "Firefox", "Edge", "Explorer"]
    if search_engine in search_engines:
        a = eval("webdriver." + search_engine + "()")
        return a
    return -1
    '''
    El código anterior no es vulnerable a inputs arbitrarios del usuario, 
    puesto que solo llega a esta función una palabra elegida por el usuario 
    a través de un selector saneado por el programa en el main.py, donde el 
    usuario no podrá nunca insertar código interpretable pues dará lugar a un error.

    Por tanto, el siguiente código es innecesario y el anterior facilita la 
    lectura y comprensión del trabajo de la función.

    if search_engine == "Chrome":
        return webdriver.Chrome()
    if search_engine == "Safari":
        return webdriver.Safari()
    if search_engine == "Firefox":
        return webdriver.Firefox()
    if search_engine == "Edge":
        return webdriver.Edge()
    if search_engine == "Explorer":
        return webdriver.Ie()
    '''


def scroll(driver: Chrome):
    driver.execute_script("""scrollBy({top:1500, left:0, behavior: "smooth"});""")
    wait(1)
    driver.execute_script("""scrollBy({top:-1500, left:0, behavior: "smooth"});""")


def massive_scroll(driver: Chrome):
    driver.execute_script("""scrollBy({top:100000000000, left:0, behavior: "smooth"});""")

    
