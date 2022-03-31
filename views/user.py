import pdb
import sqlalchemy
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.user import User
from utils.data_change import to_json
from views.base_view import list_model,delete_model,create_model,patch_model,method_not_surpport_model


@app.route('/user',methods=['GET','POST','DELETE','PATCH'])
def user():
    if request.method == 'GET':
        return list_model(User,request.args.to_dict())
    elif request.method == 'PATCH':
        data = request.json
        return patch_model(User,data,request.args.to_dict(),db)
    elif request.method == 'POST':
        data = request.json
        return create_model(User,data,db)
    elif request.method == 'DELETE':
        return delete_model(User,db,request.args.to_dict())
    else:
        return method_not_surpport_model()
