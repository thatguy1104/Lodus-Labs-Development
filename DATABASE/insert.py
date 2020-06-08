import psycopg2

conn = psycopg2.connect(database="d48rv6m38ss0k6", user="nllltklgitidxv",
                        password="95aa107e5287dda564e9021e01c05298d26a2f2b455629b489ee2cd36987ed89", host="ec2-54-247-78-30.eu-west-1.compute.amazonaws.com", port="5432")
print ("Opened database successfully")

cur = conn.cursor()

# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (1, 'Paul', 32, 'California', 20000.00 )")

# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")

# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")

# cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
#       VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
    
cur.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (5, 'Albert', 19, 'Moscow ', 100000.00 )")

conn.commit()
print ("Records created successfully")
conn.close()
