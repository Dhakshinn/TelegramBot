def add_dob(name,date,month):
    import sqlite3
    conn = sqlite3.connect('Hello.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS dob(name text,date int,month int )")
    c.execute("INSERT INTO dob(name,date,month) VALUES (?,?,?)",(name,date,month))
    conn.commit()
    c.close()
    conn.close()

def del_dob(na):
    import sqlite3
    conn = sqlite3.connect('Hello.db')
    c = conn.cursor()
    c.execute("DELETE FROM dob WHERE name=?",(na,))
    conn.commit()
    c.close()
    conn.close()

def list_dob():
    import sqlite3
    conn = sqlite3.connect('Hello.db')
    c = conn.cursor()
    c.execute("SELECT name,date,month FROM dob")
    name=[]
    date=[]
    month=[]
    for x,y,z in c.fetchall():
         name.append(x)
         date.append(y)
         month.append(z)
    return name,date,month

def Bday(d,m):
    import sqlite3
    conn = sqlite3.connect('Hello.db')
    c = conn.cursor()
    c.execute("SELECT name FROM dob WHERE date==? AND month==?",(d,m))
    name=[]
    for x in c.fetchall():
        name.append(x)
    return name