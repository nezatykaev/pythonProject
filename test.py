import pymysql

con = pymysql.connect(host='localhost',
                      port=3306,
                      user='1detailing',
                      password='Y9lCTqy7qTvDZ7O',
                      database='1detailing',
                      )

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM news_pars")

    rows = cur.fetchall()

    for row in rows:
        print("{0} {1} {2}".format(row[0], row[1], row[2]))
    con.close()