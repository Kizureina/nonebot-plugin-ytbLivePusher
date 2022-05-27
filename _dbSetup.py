import sqlite3

con = sqlite3.connect("vtb.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS ytb(id INTEGER PRIMARY KEY,url TEXT,times INTEGER)")
cur.execute('INSERT INTO ytb VALUES(?,?,?)',(124,'https://www.youtube.com/channel/UCGcD5iUDG8xiywZeeDxye-A',0))
con.commit()
cur.execute("CREATE TABLE IF NOT EXISTS users(num INTEGER PRIMARY KEY,qqid INTEGER)")
cur.execute('INSERT INTO users VALUES(?,?)',(124,1111111111))
con.commit()
cur.close()
con.close()
