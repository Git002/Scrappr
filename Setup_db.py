import sqlite3

conn = sqlite3.connect(r'test.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE Classes (id VARCHAR(30));""")
cur.execute("""INSERT INTO Classes VALUES ("question-hyperlink");""")
cur.execute("""INSERT INTO Classes VALUES ("excerpt");""")
cur.execute(
    """INSERT INTO Classes VALUES ("pl8 js-gps-track nav-links--link");""")
conn.commit()
cur.execute("""select count(*) from Classes;""")
for class_Names in cur.fetchall():
    print(class_Names)
