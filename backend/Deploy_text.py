from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)  # 1. 必须在 app.run() 之前初始化

# 2. 使用 os.path 处理路径，兼容性更好
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "My_blog_texts.sqlite")


def get_db_connection():
    """获取数据库连接，使用行工厂以便通过列名访问"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def insert_article(data):
    """数据库插入逻辑"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 3. 处理 tags：使用 json.dumps 转换为标准 JSON 字符串
        tags_json = json.dumps(data.get('tags', []), ensure_ascii=False)

        # 4. 参数化查询 (防止 SQL 注入)
        sql = """
              INSERT INTO articles
                  (title, content, status, tags, author_id, created_at, update_time)
              VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now')) \
              """

        # 默认 author_id 为 1，可根据实际登录用户修改
        cursor.execute(sql, (
            data['title'],
            data['content'],
            data.get('status', 'draft'),
            tags_json,
            1
        ))

        conn.commit()
        conn.close()
        return True, None
    except sqlite3.Error as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


@app.route('/api/deploy', methods=['POST'])  # 5. 通常发布文章只用 POST
def api_texts():
    try:
        json_data = request.get_json()

        # 6. 基础验证
        if not json_data or 'title' not in json_data or 'content' not in json_data:
            return jsonify({"error": "Missing title or content"}), 400

        success, error = insert_article(json_data)

        if success:
            return jsonify({"message": "Article published successfully"}), 201
        else:
            print(f"DB Error: {error}")
            return jsonify({"error": "Database insertion failed", "detail": error}), 500

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # 确保 data 目录存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    app.run(debug=True, port=5001)