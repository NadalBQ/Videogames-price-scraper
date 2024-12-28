import time
import json

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