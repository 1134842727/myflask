from app import db,app
from models.user import User
from models.role import Role
from views.base_view import create_model,list_model
import pdb
print("开始初始化数据库，请提前创建好空数据库！")
db.drop_all()
db.create_all()
print("初始化数据库表完毕！")
with app.app_context():
    # 创建初始角色super_admin、admin、member
    create_model(Role,{'name':'super_admin'},db)
    create_model(Role,{'name':'admin'},db)
    create_model(Role,{'name':'member'},db)
    # 创建初始用户（super_admin）
    super_admin_role = list_model(Role,{'name':'super_admin'})
    
    super_admin_role_id = super_admin_role.json.get('data')[0].get('id')
    create_model(User,{'username':'super_admin','password':'super_admin','role_id':super_admin_role_id},db)
    print('创建初始化角色：super_admin、admin、member 成功！')
    print('创建初始化用户：super_admin 成功！密码为：super_admin')
