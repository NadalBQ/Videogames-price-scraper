import json
from typing import Dict



def _get_paths():
    import glob
    paths = []
    for filepath in glob.iglob('jsons/*.json'):
        if filepath == 'jsons/games.json':
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
                            if v == dic_games[k]:
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
            gen_json(sort(dic_games))
        else:
            json.dump(dic_games, outfile)



