import sqlalchemy
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.role import Role
from utils.data_change import to_json
from views.base_view import list_model,delete_model,create_model,method_not_surpport_model,patch_model
@app.route('/role',methods=['GET','POST','DELETE','PATCH'])
def role():
    if request.method == 'GET':
        return list_model(Role,request.args.to_dict())
    elif request.method == 'PATCH':
        data = request.json
    elif request.method == 'POST':
        data = request.json
        return create_model(Role,data,db)
    elif request.method == 'DELETE':
        return delete_model(Role,db,request.args.to_dict())
    else:
        return method_not_surpport_model()
