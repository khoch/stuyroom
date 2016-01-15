import mysql.connector



cnx = mysql.connector.connect(user='nicholas', password='stuyroom', host='127.0.0.1',
                              database='test')
try:
  cnx = mysql.connector.connect(user='scott',
                                database='testt')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()



'''
Stores room, club leader name, club name, email, date, (also adds room to taken list)

Takes date and returns rooms available

Takes date and returns rooms are taken and club that took each one (2d list)


                              '''
