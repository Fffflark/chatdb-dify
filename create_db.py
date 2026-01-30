import pandas as pd
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

password = os.getenv('SQL_DB_KEY')

def create_db(out_table:pd.DataFrame)->str:
    
    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': password,
        'database': 'test_table',
        'charset': 'utf8mb4'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    print("创建 merged_access_personnel 表...")
        
    # 定义表结构（根据你的需求调整）
    create_table_query = """
        CREATE TABLE IF NOT EXISTS merged_access_personnel (
            序号 VARCHAR(20),
            卡编号（印刷在卡上的数字串） VARCHAR(50),
            RFID卡号 VARCHAR(50),
            二维码信息 TEXT,
            姓名 VARCHAR(100),
            性别 VARCHAR(10),
            岗位类别编号 VARCHAR(50),
            岗位类别 VARCHAR(100),
            单位名称 VARCHAR(200),
            职务 VARCHAR(100),
            身份证号 VARCHAR(50),
            2寸证件照（白底） VARCHAR(200),
            联系方式 VARCHAR(50),
            证件类型 VARCHAR(50),
            通行规则 VARCHAR(100),
            是否激活 VARCHAR(10),
            备注 TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (卡编号（印刷在卡上的数字串）)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        
    # 如果表已存在，先删除
    cursor.execute("DROP TABLE IF EXISTS merged_access_personnel")
        
    # 创建新表
    cursor.execute(create_table_query)
    print("表结构创建成功")
        
    # 构建INSERT语句
    columns_str = ', '.join([f'`{col}`' for col in out_table.columns])
    placeholders = ', '.join(['%s'] * len(out_table.columns))
    insert_query = f"INSERT INTO merged_access_personnel ({columns_str}) VALUES ({placeholders})"
        
    # 批量插入数据
    batch_size = 100  # 每批插入100条
    inserted_count = 0
        
    for i in range(0, len(out_table), batch_size):
        batch = out_table.iloc[i:i+batch_size]
            
        # 准备批量数据
        batch_values = []
        for _, row in batch.iterrows():
            # 将每行数据转为元组，并处理NaN值
            row_values = []
            for val in row:
                if pd.isna(val) or str(val).strip() == '' or str(val) == 'nan':
                    row_values.append(None)
                else:
                    row_values.append(str(val).strip())
            batch_values.append(tuple(row_values))
            
        # 执行批量插入
        cursor.executemany(insert_query, batch_values)
        connection.commit()
            
        inserted_count += len(batch_values)
        print(f"  已插入 {inserted_count}/{len(out_table)} 条记录...")
    
        