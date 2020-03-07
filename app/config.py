from sqlalchemy import create_engine

# 初始化数据库连接
# 按实际情况依次填写MySQL的用户名、密码、IP地址、端口、数据库名
def get_db_engine():
    return create_engine('mysql+pymysql://root:123456@localhost:3306/stock_data_cn')