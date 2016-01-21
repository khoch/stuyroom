import mysql.connector
from mysql.connector import errorcode

reservations = 'CREATE TABLE reservations (roomNum int(3), date date, clubName varchar(10), clubLeader varchar(10), email varchar(10))'
rooms  = 'CREATE TABLE rooms (roomNum int(3))'



# <-------------- Initialization -------------->
def createDB(c):
    try:
        c.execute("CREATE DATABASE stuyroom DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: stuyroom".format(err))
        exit(1)
        
def createTables(c):
    try:
        print("Creating table reservations, rooms")
        c.execute(reservations)
        c.execute(rooms)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("Created tables")
  
try:
  cnx = mysql.connector.connect(user='nicholas', password='stuyroom', host='127.0.0.1',
                                )
  cursor = cnx.cursor()
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

createTables(cursor)



# <-------------- Reservations -------------->
# roomNum, date, clubName, clubLeader, email 
def addReservation(roomNum, date, clubName, clubLeader, email):
# Inputs should be sanitized already
#    print "Adding %s, %s, %s, %s, %s" % (roomNum, date, clubName, clubLeader, email)
    input = 'INSERT INTO reservations VALUES (%s, "%s", "%s", "%s", "%s");' % (roomNum, date, clubName, clubLeader, email)
    print input
    cursor.execute(input)

def getUnavailableRooms():
    out = cursor.execute("SELECT roomNum FROM reservations")
    print out
    return out

# <-------------- Testing -------------->
def testAddReservation():
    addReservation(555, "2015-01-01", "ClubClub", "ClubLeader", "Nick@nicholasyang.com")
    getUnavailableRooms()

'''
Stores room, club leader name, club name, email, date, (also adds room to taken list)

Takes date and returns rooms available

Takes date and returns rooms are taken and club that took each one (2d list)


                              '''
