import time

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

