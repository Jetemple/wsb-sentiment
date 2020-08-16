import sqlite3

from sqlite3 import Error

def sql_connection():

    try:

        con = sqlite3.connect('mydatabase.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    # cursorObj.execute("CREATE TABLE employees(id integer PRIMARY KEY, name text, salary real, department text, position text, hireDate text)")
    # cursorObj.execute("INSERT INTO stocks VALUES ('aapl', 2)")
    cursorObj.execute("INSERT INTO comments VALUES ('g4344', 2, 'tsla')")

    con.commit()

# con = sql_connection()


def addComment(id, date, ticker):
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute("INSERT INTO comments VALUES (?, ?, ?)",(id, date, ticker))
        con.commit()
    except:
        print("Skipped")

def addPost(id, comment_count, date):
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute("INSERT INTO posts VALUES (?, ?, ?)",(id, comment_count, date))
        con.commit()
        return True
    except:
        print("Skipped")

def addTicker(ticker):
    try:
        con = sql_connection()
        cursorObj = con.cursor()
        cursorObj.execute("INSERT INTO stocks VALUES (?)",([ticker]))
        con.commit()
    except:
        print("STOCK ALREADY IN THERE")


def checkTicker(ticker):
    ticker = ticker.upper()
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("SELECT COUNT(1) FROM stocks WHERE ticker = ?",([ticker]))
    con.commit()
    val = cursorObj.fetchone()[0]
    print(val)
    if(val == 0):
        return False
    return True
    
def checkComment(id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("SELECT COUNT(1) FROM comments WHERE comment_id = ?",([id]))
    con.commit()
    val = cursorObj.fetchone()[0]
    print(val)
    if(val == 0):
        return False
    return True

def getCommentCount(id):
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute("SELECT comment_count FROM posts WHERE post_id = ?",([str(id)]))
    con.commit()
    val = cursorObj.fetchone()[0]
    print(val)
    return val

    

# con = sql_connection()
# cursorObj = con.cursor()
# cursorObj.execute("SELECT COUNT(1) FROM stocks WHERE ticker = 'TSLA'")
# print(cursorObj.fetchone()[0])
# con.commit()

# print(checkComment("g1riw6c"))
# print(checkTicker("tsla"))
# addTicker("tsla")
# sql_table(con)

# getCommentCount("ib0hti")