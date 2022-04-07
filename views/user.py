import pdb
import time
import sqlalchemy
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.user import User
from models.role import Role
from utils.data_change import to_json
from views.base_view import list_model,delete_model,create_model,patch_model,method_not_surpport_model
from utils.pyjwt import assert_jwt, set_jwt
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
                return func(role_name,*args, **kwargs)
            else:
                return func('member',*args, **kwargs)
        else:
            return 'token无效'
    return main_func


@app.route('/user',methods=['GET','POST','DELETE','PATCH'])
@certification
def user(role_name):
    if request.method == 'GET':
        hide_key_list = []
        if role_name != 'super_admin':
            hide_key_list.append('password')
        return list_model(User,request.args.to_dict(),hide_key_list)
    elif request.method == 'PATCH':
        data = request.json
        # 只有超管可以自定义role
        if role_name != 'super_admin':
            del data['role_id']
        if 'role_id' in data:
            role = list_model(Role,{'id':data.get('role_id')})
            if role.json.get('data') == []:
                return 'role_id {0} 不存在！'.format(data.get('role_id'))
        return patch_model(User,data,request.args.to_dict(),db)
    elif request.method == 'POST':
        data = request.json
        # 只有超管可以自定义role
        if role_name != 'super_admin':
            del data['role_id']
        if 'role_id' not in data:
            role = list_model(Role,{'name':'member'})
            role_id = role.json.get('data')[0].get('id')
            data['role_id'] = role_id
        else:
            role = list_model(Role,{'id':data.get('role_id')})
            if role.json.get('data') == []:
                return 'role_id {0} 不存在！'.format(data.get('role_id'))
        return create_model(User,data,db)
    elif request.method == 'DELETE':
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

@app.route('/test_certification',methods=['GET'])
@certification
def test_certification(role):
    return '认证成功，role name为'+role