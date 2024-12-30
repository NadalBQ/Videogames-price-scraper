import scrapers
import scrapers.steam
import scrapers.steam.steam_scraper

options = ["Update database", "Filter games", "Search"]
search_engines = ["Chrome", "Safari", "Firefox", "Edge", "Explorer"]

action = -1
while action < 0:
    try:
        action = int(input(f"Choose which action you want to execute \
                           (write the number):\n1. {options[0]}\n2. \
                            {options[1]}\n3. {options[2]}\n"))
    except:
        print("The chosen action couldn't be interpreted, please insert a number between 1 and 3")

if action == 1:
    try:
        search_engine = int(input(f"Which search engine do you want to make use of to \
                                proceed with the scraping? (write the number):\n\
                                1. {search_engines[0]}\n2. {search_engines[1]}\n3. {search_engines[2]}\n\
                                    4. {search_engines[3]}\n5. {search_engines[4]}\n")) - 1
    
        scrapers.steam.steam_scraper.steam_multiple_scrape(search_engines[search_engine]) # scrape all games from all categories from steam
    
    except SyntaxError:
        print("The chosen action couldn't be interpreted, please insert a number between 1 and 5")

