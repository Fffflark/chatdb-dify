# 数据库智能查询系统

## 项目简介

基于Dify平台构建的数据库智能查询系统，能够通过自然语言自动生成SQL查询语句并返回结果。系统整合了知识库管理、代码执行代理和数据库交互功能，为用户提供便捷的数据查询体验。

### 🚀 快速开始

#### 环境要求
- Python 3.10
- MySQL 8.0+
- Dify平台

#### 配置步骤

**1. 项目初始化**
```bash
# 创建虚拟环境
python3.10 -m venv db_env

# 激活虚拟环境
# Windows:
db_env\Scripts\activate
# Linux/Mac:
source db_env/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**2. 数据库配置**
- 使用MySQL Workbench创建数据库
- 创建并编辑 .env 文件：
  ```
  SQL_DB_KEY="你的数据库密码"
  ```
- 修改数据库连接配置，编辑 app.py 和 create_db.py 中的 mysql_config：
  ```python
  mysql_config = {
      'host': '你的hostname',
      'port': '你的port',
      'user': '你的username',
      'password': password,  # 从.env文件读取
      'database': '你的database名字'
  }
  ```

**3. Dify平台连接配置**
- 修改代码执行代理，编辑 agent.py：
  ```python
  api_url = "http://你的局域网IP:5004/execute_query"
  ```
- 同步更新Dify平台：在Dify的代码执行节点中，将API URL更新为上一步设置的地址

**4. 数据准备与上传**
- 数据预处理：使用 concat_tables.py 进行数据清洗和合并，根据实际需求修改数据处理逻辑
- 数据库初始化：
  ```bash
  # 创建数据库表结构
  python create_db.py
  
  # 导入数据（根据实际需求执行）
  # 注意：需要根据表的列名调整函数参数
  ```

**5. Dify平台配置**
- 创建知识库：
  - 在Dify平台新建知识库
  - 使用默认参数
  - 上传 `表名和表结构.txt`
- 创建工作流：
  - 导入 `DB-reader.yml` 工作流配置
  - 在"知识检索"节点选择刚创建的知识库
  - 在"LLM自动生成SQL"节点选择所需的大语言模型

### 🎯 启动系统

启动Flask应用服务器：
```bash
python app.py
```
服务器将在 http://localhost:5004 启动

### 📖 使用指南

1. 在Dify平台左侧导航栏找到"DB_Reader"应用
2. 在对话界面输入自然语言查询问题，例如：
   - "显示上个月的销售总额"
   - "找出销售额最高的10个产品"
   - "统计各部门的员工数量"
3. 系统将自动：
   - 理解查询意图
   - 生成相应的SQL语句
   - 执行查询并返回结构化结果

### 🔧 高级配置

**自定义数据处理**
如需自定义数据处理逻辑：
1. 修改 concat_tables.py 中的数据处理函数
2. 调整数据合并和清洗策略
3. 更新数据库表结构（需同步更新知识库文档）

**调整查询逻辑**
- 修改 agent.py 中的查询执行逻辑
- 调整SQL生成和结果处理流程

**性能优化**
- 配置数据库索引
- 调整查询缓存策略
- 优化知识库检索参数

### 🐛 故障排除

**常见问题**

1. **数据库连接失败**
   - 检查MySQL服务状态
   - 验证连接参数和密码
   - 确认网络连通性

2. **Dify连接异常**
   - 确认agent服务已启动
   - 检查防火墙设置
   - 验证API URL配置

3. **SQL生成错误**
   - 更新知识库中的表结构信息
   - 调整LLM模型参数
   - 检查查询语句的复杂度

**日志查看**
- 应用日志：查看 app.py 控制台输出
- 数据库日志：查看MySQL错误日志
- Dify日志：在Dify平台查看执行记录

### 📁 项目结构
```
CHATDB-DIFY/
├── app.py              # 主应用入口
├── agent.py            # Dify代理服务
├── create_db.py        # 数据库初始化
├── concat_tables.py    # 数据预处理
├── requirements.txt    # 项目依赖
├── DB-reader.yml       # Dify工作流配置
├── 表名和表结构.txt     # 知识库文档
└── README.md           # 项目说明
```

### ⚠️ 注意事项

**安全性**
- 妥善保管数据库密码
- 限制数据库访问权限
- 定期更新依赖包

**数据一致性**
- 数据更新后需同步更新知识库
- 定期备份数据库
- 监控查询性能

**版本兼容性**
- 确认Python版本为3.10
- 检查Dify平台版本兼容性
- 验证MySQL驱动版本