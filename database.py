import mysql.connector
from mysql.connector import errorcode


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
  print "shit works"
  

def createDB(cursor):
    try:
        cursor.execute("CREATE DATABASE stuyroom DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
        
def createTable ():
    cursor.execute('CREATE TABLE reservations (roomNum int(3), date date, clubName varchar(10), clubLeader varchar(10), email varchar(10))')
    print "initialized"

def addReservation():
  cursor.execute('ADD



'''
Stores room, club leader name, club name, email, date, (also adds room to taken list)

Takes date and returns rooms available

Takes date and returns rooms are taken and club that took each one (2d list)


                              '''
