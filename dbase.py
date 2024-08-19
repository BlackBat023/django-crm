import mysql.connector

data_base = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Dune11@#",
    auth_plugin='mysql_native_password',
)

# setup cursor object
cursorObject = data_base.cursor()

# create database
cursorObject.execute("CREATE DATABASE dccrm")

print("Database Created!")

