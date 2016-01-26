# StuyRoom
A room reservation system for Stuy.
Club/Pub Room Sign Up Website

**Link**: http://stuyroom.nicholasyang.com/

**Demo video**:  http://youtube.com/watch?v=VZfePD8VG6E


##Project Description

###Summary
A simple, user friendly way to reserve rooms for club/pub activities. Features a calendar with available dates.
Upon clicking on the calendar, a list of available rooms and unavailable rooms appears. The available rooms then link to a form for reserving them. There is also an administrator panel (still under development) which allows admins to log in and manually delete room reservations if ever necessary. Admins can also block rooms from being reserved for any period of time if another school organization (such as ARISTA) will be using them.

###TODO
* fix a few bugs that affect how available rooms are displayed
* secure the backend to ensure that nobody can ever reserve the same room twice on the same day
* finish the admin panel and optimize it for ease of used
* Deploy on SU website!

###Tools Used

* Developed in python and jquery using MySQL for data storage
* Flask
* MySQL
	* Python MySQL connector
* Hashlib
* See requirements.txt for complete list of modules used

##Instructions to run
Connection to the database is necessary but otherwise to run install the modules in requirements.txt and run app.py


##Roles:

**Leader**: Krzysztof Hochlewicz

**Backend**: Nicholas Yang

**Middleware/Frontend**: Daisy Barbanel
