import json
from typing import Dict



def _get_paths() -> list:
    import glob
    paths = []
    for filepath in glob.iglob('jsons/*.json'):
        if filepath == 'jsons/games.json' or filepath == 'jsons\\games.json' or filepath == 'jsons\\metacriticGames.json' or filepath == 'jsons/metacriticGames.json':
            pass
        else:
            paths.append(filepath)
    return paths


def _merge(paths=_get_paths()):
    dic_games = {}
    more_games = {}
    with open(paths[0], 'r', encoding='utf-8') as current:
        
        dic_games:Dict[str, list] = json.loads(current.read())

        for k, v in dic_games.items():
            dic_games[k] = [v]
        for i in range(len(paths)):
            if i == 0:
                pass
            else:
                with open(paths[i], 'r', encoding='utf-8') as other:
                    more_games:dict = json.loads(other.read())
                    for k,v in more_games.items():
                        if k in dic_games.keys():
                            if v in dic_games[k]:
                                pass
                            else:
                                dic_games[k].append(v)
                        else:
                            dic_games[k] = [v]
    return dic_games


def json_to_dict(json_path="jsons/games.json"):
    with open(json_path, 'r', encoding='utf-8') as games:
        dic_games:Dict[str, list] = json.loads(games.read())
    return dic_games


def sort(dic_games:dict):
    new_dic = {}
    keys = sorted(dic_games.keys())
    for k in keys:
        new_dic[k] = dic_games[k]
    return new_dic


def gen_json(sorted=False, dic_games:Dict[str, list]=_merge()):
    with open("jsons/games.json", "w+") as outfile:
        if sorted:
            gen_json(False, sort(dic_games))
        else:
            json.dump(dic_games, outfile)


def add_values(destination:str = "jsons/games.json", source:str = "jsons/metacriticGames.json"):
    games = json_to_dict(destination)
    source_games = json_to_dict(source)
    for k,v in games.items():
        if k in source_games.keys():
            if source_games[k] in v:
                pass
            else:
                games[k].append(source_games[k])
    for k,v in source_games.items():
        if k in games:
            pass
        else:
            games[k] = [source_games[k]]
    with open(destination, "w+") as outfile:
        json.dump(games, outfile)

def fuse_jsons(name:str = "steam"):
    import glob
    paths = []
    for filepath in glob.iglob(f'jsons/{name}*.json'):
        if filepath == f'jsons/{name}Games.json' or filepath == f'jsons\\{name}Games.json':
            pass
        else:
            paths.append(filepath)
    
    games = json_to_dict(paths[0])
    for i in range(len(paths)):
        if i == 0:
            pass
        else:
            source_games = json_to_dict(paths[i])

            for k,v in source_games.items():
                if k in games.keys():
                    pass
                else:
                    games[k] = [v]
    with open(f'jsons/{name}Games.json', "w+") as outfile:
        json.dump(games, outfile)
