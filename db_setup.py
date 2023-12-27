import sqlite3
'''
data structure:
    user: {
        id:int (UNIQUE)),
        scrap_time: datetime,
        uuid: str(UNIQUE),
        username: str (UNIQUE),
        link: str (UNIQUE),
        intralink: str (NULLABLE),
        level: int,
    }
    ranking: {
        id:int (UNIQUE),
        uuid: str(NOT UNIQUE),
        user_id:int (foreign key) (NOT UNIQUE),
        scrap_time:datetime,
        creation_time:datetime,
        percentage:int,
        score:int,
        league:str,
        league_id:int,
        global_rank:int,
        school_rank:int,
        language:str,
    }
'''


if __name__ == '__main__':
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user
                (id INTEGER PRIMARY KEY, scrap_time DATETIME, uuid TEXT UNIQUE, username TEXT UNIQUE)''') 
    c.execute('''CREATE TABLE IF NOT EXISTS ranking
                (id INTEGER PRIMARY KEY,
                uuid TEXT, user_id INTEGER, scrap_time DATETIME, creation_time DATETIME, percentage INTEGER, score INTEGER, league TEXT,league_id INTEGER, global_rank INTEGER, school_rank INTEGER, language TEXT)''')
    conn.commit()
    conn.close()