import sqlite3
#from passlib.hash import pbkdf2_sha256

def Login(username, password):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    user = username
    passw = password
    params = (user, passw)
    c.execute('SELECT * FROM users WHERE user=? and pass=?', params)
    check = c.fetchall()
    if check:
        return True
    else:
        return False