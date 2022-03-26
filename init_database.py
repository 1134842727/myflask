from app import db
print("开始初始化数据库，请提前创建好空数据库！")
db.drop_all()
db.create_all()
print("初始化数据库表完毕！")