
import scrapers.instant_gaming_scraper as instant_gaming_scraper
import scrapers.steam_scraper as steam_scraper
import scrapers.eneba_scraper as eneba_scraper
import jsons.json_aids as json_aids



def console_enter(amount:int):
    print("\n"*amount)


def main(action: int = -1):
    while action < 0:
        console_enter(5)
        try:
            action = int(input(f"Choose which action you want to execute. (write the number):\n1. {options[0]}\n2. {options[1]}\n3. {options[2]}\n4. {options[3]}\n"))

        except:
            print("The chosen action couldn't be interpreted, please insert a number between 1 and 3")
    return action


options = ["Update database", "Filter games", "Search", "Exit"]
search_engines = ["Chrome", "Safari", "Firefox", "Edge", "Explorer"]
platforms = ["Steam", "Epic-Games", "Eneba", "Instant-Gaming"]
action = main()
while True:
    if action == 1:
        console_enter(5)
        try:
            search_engine = search_engines[int(input(f"Which search engine do you want to make use of to proceed with the scraping? (write the number):\n1. {search_engines[0]}\n2. {search_engines[1]}\n3. {search_engines[2]}\n4. {search_engines[3]}\n5. {search_engines[4]}\n")) - 1]
        
            steam_scraper.steam_multiple_scrape(search_engine) # scrape all games from all categories from steam
            instant_gaming_scraper.instant_gaming_scrape(search_engine)
            eneba_scraper.eneba_scrape()

            json_aids.gen_json(sorted=True)
            console_enter(2)
            print("Database updated successfully!")
            action = main()

        except SyntaxError:
            print("The chosen action couldn't be interpreted, please insert a number between 1 and 5.")


    if action == 2:
        console_enter(5)
        try:
            platform = platforms[int(input(f"Which platform do you want to see the games of? (write the number):\n1. {platforms[0]}\n2. {platforms[1]}\n3. {platforms[2]}\n4. {platforms[3]}\n")) - 1]

            games = json_aids.json_to_dict()
            platform_games = {}
            for k, v in games.items():
                if platform in [elem[1] for elem in v]:
                    platform_games[k] = v
            
            print("All games from", platform, "have been displayed.")
            action = main()

        except SyntaxError:
            print("The chosen action couldn't be interpreted, please insert a number between 1 and 4.")

    if action == 3:
        try:
            games = json_aids.json_to_dict()
            gameName = input("What is the game you are looking for called?\n")
            keys = []
            similar = []
            theGame = False
            for key in games.keys():
                if gameName.lower() == key.lower():
                    theGame = True
                    gameName = key
                if gameName.lower() in key.lower():
                    keys.append(key)
                if key.lower() in gameName.lower():
                    similar.append(key)
            

            if not theGame:
                print("Found:")
                for key in keys:
                    print(key, games[key])
            else:
                print("Found:")
                print(gameName, games[gameName])
                see = input("Want to see games with similar names? (or different spelling)\nY/N")
                if see.lower() == "yes" or see.lower() == "y":
                    print("Similarly named games found:")
                    for key in keys:
                        print(key, games[key])
                
            see = input("Want to see games with similar names? (or different spelling)\nY/N")
            if see.lower() == "yes" or see.lower() == "y":
                print("Similarly named games found:")
                for key in similar:
                    print(key, games[key])

            print("All games with a name similar to the one written have been displayed.")
            action = main()

        except:
            print("The name you wrote can't be interpreted, try with different spelling.")

    if action == 4:
        break
