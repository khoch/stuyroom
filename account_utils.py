import sqlite3
from passlib.hash import pbkdf2_sha256

def Login(username, password):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    hash = pbkdf2_sha256.encrypt(password, rounds=20000, salt_size=16)
    #print hash
    #c.execute('INSERT INTO users VALUES(?, ?)', (username, hash))
    #c.execute('DELETE FROM users WHERE user=?', (username,))
    c.execute('SELECT * FROM users WHERE user=?', (username,))
    #conn.commit()
    storedhash = c.fetchall()
    #print storedhash
    #print "test"
    if storedhash:
        storedhash = storedhash[0][1]
        #print storedhash
        #print pbkdf2_sha256.verify(password, storedhash)
        return pbkdf2_sha256.verify(password, storedhash)
    else:
        return False
  
def ChangePass(username, newpassword):
    conn = sqlite3.connect("accounts.db")
    c = conn.cursor()
    hash = pbkdf2_sha256.encrypt(newpassword, rounds=20000, salt_size=16)
    c.execute('UPDATE users SET pass=? WHERE user=?', (hash, username))
    conn.commit()

  