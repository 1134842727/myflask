
from flask import request
from config.http_code import *
from app import app,db
from models.role import Role
from views.base_view import list_model,delete_model,create_model,method_not_surpport_model,patch_model

from views.user import certification
@app.route('/role',methods=['GET','POST','DELETE','PATCH'])
@certification
def role(username,role_name):
    if request.method == 'GET':
        return list_model(Role,request.args.to_dict())
    elif request.method == 'PATCH':
        if role_name != "super_admin":
            return '只有超管可以使用此接口方法'
        data = request.json
    elif request.method == 'POST':
        if role_name != "super_admin":
            return '只有超管可以使用此接口方法'
        data = request.json
        return create_model(Role,data,db)
    elif request.method == 'DELETE':
        if role_name != "super_admin":
            return '只有超管可以使用此接口方法'
        return delete_model(Role,db,request.args.to_dict())
    else:
        return method_not_surpport_model()
