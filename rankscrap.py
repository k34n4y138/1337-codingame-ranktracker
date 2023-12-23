# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rankscrap.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: zmoumen <zmoumen@student.1337.ma>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/23 14:58:28 by zmoumen           #+#    #+#              #
#    Updated: 2023/12/23 14:58:56 by zmoumen          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import requests, datetime, os

LEAGUES =["WOOD 3", "WOOD 2", "WOOD 1", "BRONZE", "SILVER", "GOLD", "LEGEND"]

LINK = "https://www.codingame.com/services/Leaderboards/getFilteredChallengeLeaderboard"

BODY = ["fall-challenge-2023","fdad4e510321da452fcccccc7e268cf40952875","school",{"active":False,"column":"","filter":""}]
CSV_HEADER = "USERNAME|GLOBAL RANK|SCHOOL RANK|LEAGUE|SCORE|last activity|status"
CELL_WIDTH = 20


def fixate_cellwidth(data, align="center"):
    if align == "center":
        data = data.center(CELL_WIDTH)
    elif align == "left":
        data = data.ljust(CELL_WIDTH)
    elif align == "right":
        data = data.rjust(CELL_WIDTH)
    if len(data) > CELL_WIDTH:
        data = data[:CELL_WIDTH - 3] + "..."
    return data

def epocher(milisecs: str):
    return datetime.datetime.fromtimestamp(int(milisecs)/1000).strftime("%m/%d %H:%M")


def get_ranking():
    response = requests.post(LINK, json=BODY)
    data = response.json()
    ranking = []    
    for user in data['users']:
        print(user)
        line = '|' + fixate_cellwidth(user['pseudo'],'left') + '|'
        line += fixate_cellwidth(str(user['globalRank'])) + '|'
        line += fixate_cellwidth(str(user['rank'])) + '|'
        line += fixate_cellwidth(LEAGUES[user['league']['divisionIndex']]) + '|'
        line += fixate_cellwidth(str(user['score'])) + '|'
        line += fixate_cellwidth(epocher(user['creationTime'])) + '|'
        line += fixate_cellwidth("stable" if user['percentage'] >= 100 else f"PROGRESSING![{user['percentage']}%]") + '|'
        ranking.append(line)
        
    return ranking

if __name__ == "__main__":
    ranking = get_ranking()
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    fname = "ranking-" + date + ".txt"
    file = open(fname, "w")
    header = '|' + ''.join([fixate_cellwidth(x) + '|' for x in CSV_HEADER.split('|')])
    splitter = ' ' + ' '.join(['-'*(CELL_WIDTH) for x in CSV_HEADER.split('|')])
    file.write(header + "\n" + splitter + "\n")
    for line in ranking:
        file.write(line + "\n" + splitter + "\n")
    file.close()
    os.system(f"open {fname}")
    print("DONE!")
    
