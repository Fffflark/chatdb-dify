from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import concat_tables
import create_db
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv('SQL_DB_KEY')
def get_db_connection():
    mysql_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': password,
        'database': 'test_table'
    }
    return mysql.connector.connect(**mysql_config)
def main(origin_path,expand_path):
    # 初始化 Flask 应用
    get_db_connection()
    app = Flask(__name__)
    df = concat_tables.concat_tables(origin_path, expand_path)
    create_db.create_db(df)

    # 处理 /execute_query 路由
    @app.route('/execute_query', methods=['GET'])
    def execute_query():
        # 获取用户传入的 SQL 查询
        query = request.args.get('sql_query')
        
        if not query:
            return jsonify({'error': 'No query provided'}), 400

        # 连接到数据库并执行查询
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(query)
            data = cur.fetchall()
            cur.close()
            conn.close()
            return jsonify(data)
        
        except Exception as e:
            if conn:
                conn.close()
            return jsonify({'error': str(e)}), 500
        
    app.run(debug=True,host='0.0.0.0', port=5004)
        

# 启动 Flask 服务
if __name__ == '__main__':
    main('./人员表（伪造.xlsx', './门禁表（伪造.xlsx')