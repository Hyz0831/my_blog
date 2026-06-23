import sqlite3
conn = sqlite3.connect("data/My_blog_texts.sqlite") # 请确保路径正确
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(articles)")
columns = cursor.fetchall()
for col in columns:
    print(col) # 输出格式: (cid, name, type, notnull, dflt_value, pk)
conn.close()