import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jsn36879!",
    database='essex_online_store'
)

mycursor = db.cursor(buffered=True)
mycursor.execute("create table test (name varchar(20), email varchar(40)) ")
mycursor.execute("insert into `test` (name, email) values ('pao', 'pao@gmail.com');")
# mycursor.execute("COMMIT")
mycursor.execute("select * from `test`")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)
db.commit()
# print(data)

# /Users/chuntingjustinlo/PycharmProjects/essex_online_store