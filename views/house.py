
import pdb
import time
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.house import House
from models.img import Img
from views.base_view import list_model,delete_model,create_model,patch_model,method_not_surpport_model,list_model_simple,create_model_simple
from views.user import certification
@app.route('/house',methods=['GET','POST','DELETE','PATCH'])
@certification
def house(username,role_name):
    data = request.json
    request_args_dict = request.args.to_dict()
    if request.method == 'GET':
        return list_model(House,request_args_dict)
    elif request.method == 'POST': 
        if 'admin' not in role_name:
            return '只有管理员可用！'
        if 'cover' in data:
            img = list_model_simple(Img,{'id':data.get('cover')})
            if img.count() == 0:
                return "封面图片不存在"
            elif img.count() > 1:
                return "满足条件的图片不止一个！请检查筛选条件！"
        return create_model(House,data,db)
    elif request.method == 'PATCH':
        if 'admin' not in role_name:
            return '只有管理员可用！'
        return patch_model(House,data,request_args_dict,db)
    elif request.method == 'DELETE':
        if 'admin' not in role_name:
            return '只有管理员可用！'
        house = list_model(House,request_args_dict)
        if house.json.get('data'):
            if len(house.json.get('data')) != 1:
                return '符合条件的数据非一条，请检查筛选条件！'
        return delete_model(House,db,request_args_dict)
    else:
        return method_not_surpport_model()