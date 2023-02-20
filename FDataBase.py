import math
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []


def addPost(self, title, text):
    try:
        tm = math.floor(time.time())
        self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?)", (title, tex, tm))
        self.__db.commit()
    except sqlite3.Error as e:
        print("Ошибка добавления статьи в БД"+str(e))
        return False
    return True