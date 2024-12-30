import scrapers
import scrapers.steam
import scrapers.steam.steam_scraper

options = ["Update database", "Filter games", "Search"]
action = -1
while action < 0:
    try:
        action = int(input(f"Choose which action you want to execute (write the number):\n1. {options[0]}\n2. {options[1]}\n3. {options[2]}\n"))
    except:
        print("The chosen action couldn't be interpreted, please insert a number between 1 and 3")

if action == 1:
    scrapers.steam.steam_scraper.steam_multiple_scrape() # scrape all games from all categories from steam

