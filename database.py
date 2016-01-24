import mysql.connector
from operator import sub
from itertools import imap
from mysql.connector import errorcode

tables = {'reservations':'CREATE TABLE reservations (roomNum INT(3), date DATE, clubName VARCHAR(64), clubLeader VARCHAR(64), email VARCHAR(64))', "rooms" : 'CREATE TABLE rooms (roomNum INT(3))', 'users': 'CREATE TABLE users (username VARCHAR(64), password VARCHAR(64)), banned BOOLEAN'}
try:
  cnx = mysql.connector.connect(user='nicholas', password='stuyroom', host='127.0.0.1')
  cnx.database = "stuyroom"
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
    print("Creating...")
    createDatabase(cursor)
  else:
    print(err)
else:
  print "Databases ready"


# <-------------- Initialization -------------->

def createDB():

    cursor = cnx.cursor(buffered=True)
    try:
        cursor.execute("CREATE DATABASE stuyroom DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print("Failed creating database: stuyroom".format(err))
        exit(1)
        
def createTables():
    print("Creating table reservations, rooms, users")
    for key in tables:
        cursor = cnx.cursor(buffered=True)
        try:
            cursor.execute(tables[key])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Tables already exist.")
                getAll(key)
            else:
                print(err.msg)
        else:
            print("Created table: " + key)
        
    
  

# <-------------- Testing -------------->

def testAddReservation():
    cursor = cnx.cursor(buffered=True)
    addReservation(555, "2015-01-01", "ClubClub", "ClubLeader", "Nick@nicholasyang.com")
    return getAllReservedRooms()

def getAllReservedRooms():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT roomNum FROM reservations")
    return cursor.findall()


def get(n):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(n)
    rows = cursor.fetchall()
    print rows;
    cursor.close()

def set(n):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(n)

def getAll(key):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM " + key)
    if key == "reservations":
        for (roomNum, date, clubName, clubLeader, email) in cursor:
            print ("Room {} was reserved on {: %d %b %Y} by {} ({}) of {}".format(roomNum, date, clubLeader, email, clubName))
    if key == "users":
        for (username, passwords) in cursor:
            print ("User: {}".format(username))
    if key == "rooms":
        for (rooms) in cursor:
            print ("Room {}".format(rooms))



# <---------------------------- Reservations ---------------------------->

# <-------------- Queries -------------->
def getReservationChron():
# This is gonna be a list of tuples. Tuples suck, I know, but they can hold multiple types and are really useful
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM reservations ORDER BY date ASC;")
    return cursor.fetchall()





# <-------------- Insertion -------------->

# roomNum, date, clubName, clubLeader, email 
def addReservation(roomNum, date, clubName, clubLeader, email):
#    Inputs should be sanitized already
#    print "Adding %s, %s, %s, %s, %s" % (roomNum, date, clubName, clubLeader, email)
    cursor = cnx.cursor(buffered=True)
    input = 'INSERT INTO reservations VALUES ({}, "{}", "{}", "{}", "{}");'.format(roomNum, date, clubName, clubLeader, email)
    print input
    cursor.execute(input)
    cnx.commit()

# <-------------- Insertion -------------->

def deleteReservation(date, room):
    cursor = cnx.cursor(buffered=True)
    cursor.execute('DELETE FROM reservations WHERE date = "{}" AND room = "{}"'.format(date, room))

# <---------------------------- Rooms ---------------------------->

     

# <-------------- Queries -------------->
           
def getTakenRooms(date):
    # Gets rooms taken on a given date. Converts tuple to list
    cursor = cnx.cursor(buffered=True)
    getRooms = 'SELECT roomNum, clubName FROM reservations WHERE date = "{}";'.format(date)
    cursor.execute(getRooms)
    rooms = cursor.fetchall()
    # Don't know why I can't edit rooms to have lists instead of tuples, but I guess this works
    out = []
    for room in rooms:
        room = list(room)
        out.append(room)
    return out

def getAllRooms():
    # Gets all the rooms, puts them into a simple list
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    out = []
    for room in rooms:
        out.append(room[0])
    return out

def getAvailableRooms(date):
    # Subtracts the rooms taken from the total rooms
    takenRooms = getTakenRooms(date)
    allRooms = getAllRooms()
    return list(set(a) - set(b))


# <-------------- Insertion -------------->            

def addRoom(roomNum):
    # Adds a room, pretty self explainatory 
    cursor = cnx.cursor(buffered=True)
    cursor.execute("INSERT INTO rooms VALUES ( {} );".format(roomNum))
    cnx.commit()

# <---------------------------- Users ---------------------------->

def addUser(username, password):
    # Everything should be hashed by now
    cursor = cnx.cursor(buffered=True)
    cursor.execute('INSERT INTO users VALUES ( "{}", "{}");'.format(username, password))

def checkUser(username, password):
    # returns 0 if user exists with correct password, 1 if the password is wrong and 2 if they do not exist
    cursor = cnx.cursor(buffered=True)
    if userExists(username):
        cursor.execute('SELECT count(1) FROM users WHERE username = "{}" AND password ="{}"'.format(username, password))
        result = cursor.fetchone()
        if (result[0] == 1):
            return 0
        else:
            return 1
    return 2

def userExists(username):
    # returns false if user does not exist, true if they do
    cursor = cnx.cursor(buffered=True)
    cursor.execute('SELECT count(1) FROM users WHERE username="{}"'.format(username))
    result = cursor.fetchone()
    if result[0] == 0:
        return False
    return True


# <---------------------------- Misc ---------------------------->

def importRooms(fileName):
    rooms = open(fileName, "r")
    for room in rooms:
        addRoom(int(room))
        
        
'''
Stores room, club leader name, club name, email, date, (also adds room to taken list)

Takes date and returns rooms available

Takes date and returns rooms are taken and club that took each one (2d list)


                              '''
