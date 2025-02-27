import mysql.connector

# Replace with your actual connection details

mydb=mysql.connector.connect(host="sql7.freesqldatabase.com",user='sql7716759',password='Yb7GcYuU1K',database='sql7716759')

mycursor = mydb.cursor()

mycursor.execute("select * from cridentials")
myresult = mycursor.fetchall()

# Print the results (optional)
for row in myresult:
    print(row)

mydb.close()
