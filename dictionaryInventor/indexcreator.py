# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect("wordBank_en_ch.db")
cur = con.cursor()
cur.execute("CREATE INDEX fromwordindex ON wordTable(from_word)")
con.commit()
con.close()
