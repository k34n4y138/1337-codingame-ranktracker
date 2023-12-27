# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    rankscrap.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: zmoumen <zmoumen@student.1337.ma>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/23 14:58:28 by zmoumen           #+#    #+#              #
#    Updated: 2023/12/27 16:02:09 by zmoumen          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import requests, datetime, os, sqlite3

LEAGUES =["WOOD 3", "WOOD 2", "WOOD 1", "BRONZE", "SILVER", "GOLD", "LEGEND"]

LINK = "https://www.codingame.com/services/Leaderboards/getFilteredChallengeLeaderboard"

BODY = ["fall-challenge-2023","fdad4e510321da452fcccccc7e268cf40952875","school",{"active":False,"column":"","filter":""}]
CSV_HEADER = "USERNAME|GLOBAL RANK|SCHOOL RANK|LEAGUE|SCORE|last activity|status"
CELL_WIDTH = 20


DATABASE = sqlite3.connect('database.sqlite')

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


def fetch_ranking():
    response = requests.post(LINK, json=BODY)
    data = response.json()
    rankings = []
    for user in data['users']:
        new = {
            'user' : {
            'scrap_time':datetime.datetime.now().timestamp(), #timestamp
            'uuid': user['codingamer']['publicHandle'],
            'username':user['pseudo']
            },
            'ranking': {
            'scrap_time':datetime.datetime.now().timestamp(),
            'uuid':user['testSessionHandle'],
            'creation_time':user['creationTime'],
            'percentage': user['percentage'],
            'score': user['score'],
            'league':LEAGUES[user['league']['divisionIndex']],
            'league_id':user['league']['divisionIndex'], # 0-6
            'global_rank':user['globalRank'],
            'school_rank': user['rank'],
            'language':user['programmingLanguage'],
            }
        }
        rankings.append(new)
    return rankings


def save_user_into_db(user):
    # creates a user if not exists and returns its id
    c = DATABASE.cursor()
    c.execute("SELECT id FROM user WHERE uuid=?", (user['uuid'],))
    user_id = c.fetchone()
    if user_id is None:
        c.execute("INSERT INTO user (scrap_time, uuid, username) VALUES (?, ?, ?)", (user['scrap_time'], user['uuid'], user['username']))
        user_id = c.lastrowid
    else:
        user_id = user_id[0]
    return user_id


def save_rankings_into_db(rankings):
    c = DATABASE.cursor()
    for ranking in rankings:
        user_id = save_user_into_db(ranking['user'])
        c.execute("INSERT INTO ranking (scrap_time, uuid, user_id, creation_time, percentage, score, league, global_rank, school_rank, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (ranking['ranking']['scrap_time'], ranking['ranking']['uuid'], user_id, ranking['ranking']['creation_time'], ranking['ranking']['percentage'], ranking['ranking']['score'], ranking['ranking']['league'], ranking['ranking']['global_rank'], ranking['ranking']['school_rank'], ranking['ranking']['language']))
    DATABASE.commit()
def save_rankings_into_file(rankings):
    date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    fname = "ranking-" + date + ".txt"
    file = open(fname, "w")
    header = '|' + ''.join([fixate_cellwidth(x) + '|' for x in CSV_HEADER.split('|')])
    splitter = ' ' + ' '.join(['-'*(CELL_WIDTH) for x in CSV_HEADER.split('|')])
    file.write(header + "\n" + splitter + "\n")
    for ranking in rankings:
        line = '|' + fixate_cellwidth(ranking['user']['username'],'left') + '|'
        line += fixate_cellwidth(str(ranking['ranking']['global_rank'])) + '|'
        line += fixate_cellwidth(str(ranking['ranking']['school_rank'])) + '|'
        line += fixate_cellwidth(ranking['ranking']['league']) + '|'
        line += fixate_cellwidth(str(ranking['ranking']['score'])) + '|'
        line += fixate_cellwidth(epocher(ranking['ranking']['creation_time'])) + '|'
        line += fixate_cellwidth("stable" if ranking['ranking']['percentage'] >= 100 else f"PROGRESSING![{ranking['ranking']['percentage']}%]") + '|'
        file.write(line + "\n" + splitter + "\n")
    file.close()
    # os.system(f"open {fname}")
    print("created : " + fname)

def routine():
    ranking = fetch_ranking()
    save_rankings_into_db(ranking)
    save_rankings_into_file(ranking)
    

import time

if __name__ == "__main__":
    HOURS = 4
    while True:
        routine()
        print(f"Sleeping for {HOURS} hours")
        time.sleep(HOURS * 3600)

DATABASE.close()
