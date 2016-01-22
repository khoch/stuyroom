import mysql.connector
from operator import sub
from itertools import imap
from mysql.connector import errorcode

tables = {'reservations':'CREATE TABLE reservations (roomNum int(3), date date, clubName varchar(24), clubLeader varchar(24), email varchar(30))', "rooms" : 'CREATE TABLE rooms (roomNum int(3))', 'users': 'CREATE TABLE users (username varchar(24), password varchar(30))'}
try:
  cnx = mysql.connector.connect(user='nicholas', password='stuyroom', host='127.0.0.1',
                                )
 
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
        cursor.execute("CREATE DATABASE stuyroom DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
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
        
    
  





# <-------------- Reservations -------------->
# roomNum, date, clubName, clubLeader, email 
def addReservation(roomNum, date, clubName, clubLeader, email):
# Inputs should be sanitized already
#    print "Adding %s, %s, %s, %s, %s" % (roomNum, date, clubName, clubLeader, email)
    cursor = cnx.cursor(buffered=True)
    input = 'INSERT INTO reservations VALUES (%s, "%s", "%s", "%s", "%s");' % (roomNum, date, clubName, clubLeader, email)
    print input
    cursor.execute(input)
    cnx.commit()

def getUnavailableRooms():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT roomNum FROM reservations;")
    for roomNum in cursor:
        print roomNum


# <-------------- Testing -------------->
def testAddReservation():
    cursor = cnx.cursor(buffered=True)
    addReservation(555, "2015-01-01", "ClubClub", "ClubLeader", "Nick@nicholasyang.com")
    getUnavailableRooms()


def execute(n):
    cursor = cnx.cursor(buffered=True)
    cursor.execute(n)
    rows = cursor.fetchall()
    print rows;
    cursor.close()

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
            

# <-------------- Queries -------------->            
def getRoomsOnDate(date):
    cursor = cnx.cursor(buffered=True)
    getRooms = 'SELECT roomNum FROM reservations WHERE date = " ' + date + ' ";'
    print getRooms
    cursor.execute(getRooms)
    return cursor.fetchall()

def getAllRooms():
    cursor = cnx.cursor(buffered=True)
    cursor.execute("SELECT * FROM rooms")
    return cursor.fetchall()

def getAvailableRooms(date):
    takenRooms = getRoomsOnDate(date)
    allRooms = getAllRooms()
    a = []
    b = []
    for room in allRooms:
        a.append(room[0])
    for room in takenRooms:
         b.append(room[0])
    return list(set(a) - set(b))
  


def addRoom(roomNum):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("INSERT INTO rooms VALUES (" + str(roomNum) + ");", )
    cnx.commit()
        
'''
Stores room, club leader name, club name, email, date, (also adds room to taken list)

Takes date and returns rooms available

Takes date and returns rooms are taken and club that took each one (2d list)


                              '''
