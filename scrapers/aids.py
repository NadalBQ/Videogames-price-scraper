import time
import json
from selenium import webdriver


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


def set_driver(search_engine="Chrome"):
    '''
    search_engine must be Chrome, Edge or any search engine supported by selenium
    This function returns a webdriver
    '''
    
    # a = eval("webdriver." + search_engine + "()")   It's a vulnerability, user can insert any code, for example:
    # return a                                        "Chrome();\nimport os\nos.remove('C:\\system32'); print"
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
    
