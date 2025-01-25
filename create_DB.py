import mysql.connector



# establish connection



conn = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = 'yourPCpassword',
                               auth_plugin = 'mysql_native_password'
                               )




cur_obj = conn.cursor()

cur_obj.execute("CREATE DATABASE RideShare;")


cur_obj.execute("SHOW DATABASES;")
for row in cur_obj:
    print(row)


print(conn)
conn.close()


