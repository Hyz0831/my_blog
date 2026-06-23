from importlib.resources import contents

from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

db_path = r"E:\my_site\My_blog_api\data\My_blog_texts.sqlite"




def update_database(new_data):
    sql_words = f"""update Text_Data 
                   set content = {new_data}
                   where id = 1 and title = '智能数据可视化与后端存储一体化实践';"""
    return sql_words


@app.route('/api/texts',methods=['GET', 'POST'])
def get_texts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    content="'测试数据更新'"
    sql_words = update_database(content)
    cursor.execute(sql_words)
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)