import pdb
import time
from flask import request
from config.http_code import *
from app import app,db
from models.user import User
from models.role import Role
from models.img import Img
from views.base_view import list_model,delete_model,create_model,patch_model,method_not_surpport_model
from utils.pyjwt import assert_jwt, set_jwt
from utils.file_manager import file_upload
#部署前记得修改自己的盐
salt ='linkai4836'

from functools import wraps
def certification(func):
    @wraps(func)
    def main_func(*args, **kwargs):
        user = assert_jwt(request.headers.get('token'),salt)
        if type(user) == str:
            return 'token无效'
        username = user.get('name').get('username')
        password = user.get('name').get('password')
        user = list_model(User,{'username':username})
        if user.json.get('data') != [] and user.json.get('data')[0].get('password') == password:
            if user.json.get('data')[0].get('role_id'):          
                role = list_model(Role,{'id':user.json.get('data')[0].get('role_id')}).json.get('data')[0]
                role_name = role.get('name')
                return func(username,role_name,*args, **kwargs)
            else:
                return func('member',*args, **kwargs)
        else:
            return 'token无效'
    return main_func


@app.route('/user',methods=['GET','POST','DELETE','PATCH'])
@certification
def user(username,role_name):
    if request.method == 'GET':
        hide_key_list = []
        if role_name != 'super_admin':
            hide_key_list.append('password')
        return list_model(User,request.args.to_dict(),hide_key_list)
    elif request.method == 'PATCH':
        data = request.json
        # 只有超管可以自定义role
        if role_name != 'super_admin' and 'role_id' in data:
            del data['role_id']
        if 'role_id' in data:
            role = list_model(Role,{'id':data.get('role_id')})
            if role.json.get('data') == []:
                return 'role_id {0} 不存在！'.format(data.get('role_id'))
        if role_name != 'super_admin':
            user = list_model(User,request.args.to_dict())
            if user.json.get('data'):
                if len(user.json.get('data')) != 1:
                    return '符合条件的数据非一条，请检查筛选条件！'
                if user.json.get('data')[0].get('username') != username:
                    return '非超管只能修改自己！'
        return patch_model(User,data,request.args.to_dict(),db)
    elif request.method == 'DELETE':
        if role_name != 'super_admin':
            user = list_model(User,request.args.to_dict())
            if user.json.get('data'):
                if len(user.json.get('data')) != 1:
                    return '符合条件的数据非一条，请检查筛选条件！'
                if user.json.get('data')[0].get('username') != username:
                    return '非超管只能删除自己！'
        return delete_model(User,db,request.args.to_dict())
    else:
        return method_not_surpport_model()

@app.route('/login',methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = list_model(User,{'username':username})
    if user.json.get('data') != [] and user.json.get('data')[0].get('password') == password:
        exp_time = int(time.time()) + 480
        return set_jwt(salt,data={'username':username,'password':password},exp_time=exp_time) 
    else:
        return "用户或密码错误"

@app.route('/regist',methods=['POST'])
def regist():
    data = request.form.to_dict()
    if 'role_id' in data:
        del data['role_id']
    if 'role_id' not in data:
        role = list_model(Role,{'name':'member'})
        role_id = role.json.get('data')[0].get('id')
        data['role_id'] = role_id
    else:
        role = list_model(Role,{'id':data.get('role_id')})
        if role.json.get('data') == []:
            return 'role_id {0} 不存在！'.format(data.get('role_id'))
    # 用户注册是否传了头像
    files = request.files.getlist('img')    
    if files:
        file = files[0]
        file_url = file_upload(file)
        img = Img(url=file_url,description='user-img-' + data['username'])
        db.session.add(img)
        db.session.commit()
        data['img'] = img.id
    return create_model(User,data,db)