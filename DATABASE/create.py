import psycopg2

conn = psycopg2.connect(database="d48rv6m38ss0k6", user="nllltklgitidxv",
                        password="95aa107e5287dda564e9021e01c05298d26a2f2b455629b489ee2cd36987ed89", host="ec2-54-247-78-30.eu-west-1.compute.amazonaws.com", port="5432")
print ("Opened database successfully")

cur = conn.cursor()
cur.execute('''CREATE TABLE COMPANY
      (ID INT PRIMARY KEY     NOT NULL,
      NAME           TEXT    NOT NULL,
      AGE            INT     NOT NULL,
      ADDRESS        CHAR(50),
      SALARY         REAL);''')
print ("Table created successfully")

conn.commit()
conn.close()
