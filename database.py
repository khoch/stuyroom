import mysql.connector
import datetime
from operator import sub
from itertools import imap
from passlib.hash import pbkdf2_sha256
from mysql.connector import errorcode
from passlib.hash import pbkdf2_sha256

tables = {'reservations':'CREATE TABLE reservations (roomNum INT(4), date DATE, clubName VARCHAR(64), clubLeader VARCHAR(64), email VARCHAR(64))', "rooms" : 'CREATE TABLE rooms (roomNum INT(4))', 'users': 'CREATE TABLE users (username VARCHAR(64), password VARCHAR(256), banned BOOLEAN)'}
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
    #cursor.close()
        
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
    #cursor.close()
    
def reloadTables():
    cursor = cnx.cursor(buffered=True)
    print "Dropping reservations...."
    cursor.execute("DROP TABLE reservations;")
    print "Dropping rooms....."
    cursor.execute("DROP TABLE rooms;")
    print "Dropping users...."
    cursor.execute("DROP TABLE users;")
    print "Creating tables...."
    createTables()
    importRooms("rooms.txt")
    print "Done"
# <-------------- Testing -------------->

def testAddReservation():
    addReservation(555, "2015-01-01", "ClubClub", "ClubLeader", "Nick@nicholasyang.com")
    return getAllReservedRooms()

def getAllReservedRooms():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT roomNum FROM reservations")
    output = cursor.findall()
    cursor.close()
    return output

def get(n):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(n)
    rows = cursor.fetchall()
    print rows;
    cursor.close()

def set(n):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(n)
    cursor.close()

def getAll(key):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM " + key)
    if key == "reservations":
        for (roomNum, date, clubName, clubLeader, email) in cursor:
            print ("Room {} was reserved on {: %d %b %Y} by {} ({}) of {}".format(roomNum, date, clubLeader, email, clubName))
    if key == "users":
        for (username, passwords, banned) in cursor:
            print ("User: {}".format(username))
    if key == "rooms":
        for (rooms) in cursor:
            print ("Room {}".format(rooms))
    cursor.close()


# <---------------------------- Reservations ---------------------------->

# <-------------- Queries -------------->
def getReservationChron():
# This is gonna be a list of tuples. Tuples suck, I know, but they can hold multiple types and are really useful
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM reservations ORDER BY date ASC;")
    output = cursor.fetchall()
    #cursor.close()
    return output



# <-------------- Insertion -------------->

# roomNum, date, clubName, clubLeader, email 
def addReservation(roomNum, date, clubName, clubLeader, email):
#    Inputs should be sanitized already
#    print "Adding %s, %s, %s, %s, %s" % (roomNum, date, clubName, clubLeader, email)
    cursor = cnx.cursor(buffered=True)
    input = 'INSERT INTO reservations VALUES ({}, "{}", "{}", "{}", "{}");'.format(roomNum, date, clubName, clubLeader, email)
    print input
    cursor.execute(input)
    #cursor.close()
    cnx.commit()

# <-------------- Deletion -------------->

def deleteReservation(date, room):
    cursor = cnx.cursor(buffered=True)
    cursor.execute('DELETE FROM reservations WHERE date = "{}" AND room = "{}"'.format(date, room))
    #cursor.close()

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
    #cursor.close()
    return out

def getAllRooms():
    # Gets all the rooms, puts them into a simple list
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()
    out = []
    for room in rooms:
        out.append(room[0])
    #cursor.close()
    return out

def getAvailableRooms(date):
    # Subtracts the rooms taken from the total rooms
    cursor = cnx.cursor(buffered=True)
    getRooms = 'SELECT roomNum FROM rooms WHERE roomNum NOT IN (SELECT roomNum FROM reservations WHERE date="{}")'.format(date)
    cursor.execute(getRooms)
    rooms = cursor.fetchall()
    print rooms
    out = []
    for room in rooms:
        out.append(room[0])
    return out

'''
def getAvailableRooms(date):
    takenRooms = getTakenRooms(date)
    allRooms = getAllRooms()
    return list(set(a) - set(b))
'''

# <-------------- Insertion -------------->            

def addRoom(roomNum):
    # Adds a room, pretty self explainatory 
    cursor = cnx.cursor(buffered=True)
    cursor.execute("INSERT INTO rooms VALUES ( {} );".format(roomNum))
    cnx.commit()
    #cursor.close()

# <---------------------------- Users ---------------------------->

def addUser(username, password):
    # Everything should be hashed by now
    hashedPassword = hash(password)
    print "Added user: " + hashedPassword
    if userExists(username):
        return False
    cursor = cnx.cursor(buffered=True)
    cursor.execute('INSERT INTO users VALUES ( "{}", "{}", False);'.format(username, hashedPassword))
    cnx.commit()
    cursor.close()
    return True

def checkUser(username, password):
    # returns 0 if user exists with correct password, 1 if the password is wrong and 2 if they do not exist
    cursor = cnx.cursor(buffered=True)
    if userExists(username):
        cursor.execute('SELECT password FROM users WHERE username = "{}";'.format(username))
        result = cursor.fetchone()
        
        cursor.close()
        if pbkdf2_sha256.verify(password, result[0]):
            return 0
        else:
            return 1
    cursor.close()
    return 2

def userExists(username):
    # returns false if user does not exist, true if they do
    cursor = cnx.cursor(buffered=True)
    cursor.execute('SELECT count(1) FROM users WHERE username="{}"'.format(username))
    result = cursor.fetchone()
    cursor.close()
    if result[0] == 0:
        return False
    return True

def changePassword(username, newPassword):
    cursor = cnx.cursor(buffered=True)
    updatePassword = 'UPDATE users SET password = "{}" WHERE username = "{}"'.format(hash(newPassword), username)
    cursor.execute(updatePassword)
    cursor.close()
    
    
def getPassword(username):
    cursor = cnx.cursor(buffered=True)
    getPassword = 'SELECT password FROM users WHERE username= "{}"'.format(username)
    cursor.execute(getPassword)
    out = cursor.fetchall()
    return out[0][0]

def deleteUser(username):
    cursor = cnx.cursor(buffered=True)
    removeUser = 'DELETE FROM users WHERE username = "{}"'.format(username)
    cursor.execute(removeUser)
    cnx.commit()
# <---------------------------- Misc ---------------------------->

def importRooms(fileName):
    rooms = open(fileName, "r")
    for room in rooms:
        addRoom(int(room))

def restrictRoom(year, month, day, numOfDays, roomNum):
    t = datetime.date(year, month, day)
    for i in range (0, numOfDays):
        addReservation(roomNum, str(t), "SU", "SU", "StuyvesantStudentUnion2015@gmail.com")
        t = t + datetime.timedelta(days=1)
        print t

def hash(input):
    return pbkdf2_sha256.encrypt(input, rounds=20000, salt_size=16)
'''
Stores room, club leader name, club name, email, date, (also adds room to taken list)

Takes date and returns rooms available

Takes date and returns rooms are taken and club that took each one (2d list)


                              '''
