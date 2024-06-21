########THIS FILE HELPS US TO CREATE DATABASE AND TABLE##########################
#run apache and mysql in XAMPP and then search for,                             #
#localhost:7882/phpmyadmin ,in browser and then run this file to create database#
#################################################################################

import mysql.connector

mydb= mysql.connector.connect(host="localhost", user="root", passwd="")

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE face_reco_user")
#to create database named face_reco_user

mycursor.execute("SHOW DATABASES")

#to show availiable database list

for x in mycursor:
    print(x)

mydb= mysql.connector.connect(host="localhost", user="root", passwd="",database="face_reco_user")
mycursor = mydb.cursor()
#to get inside database face_reco_user

mycursor.execute("create table user_Table(id int primary key,Name varchar(50), Age int,Address varchar(50))")
#to create table named user_Table

mycursor.execute("show tables")
for x in mycursor:
    print(x)

#to show availiable tables in face_reco_user
