from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

db_path = r"E:\my_site\My_blog_api\data\My_blog_texts.sqlite"

@app.route('/api/texts',methods=['GET', 'POST'])
def get_texts():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Text_Data")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)