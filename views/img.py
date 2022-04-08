
from flask import request
from config.http_code import *
from app import app,db
from models.img import Img
from views.base_view import list_model,delete_model,method_not_surpport_model
from utils.file_manager import file_delete
from views.user import certification
import pdb
@app.route('/img',methods=['GET','DELETE'])
@certification
def img(username,role_name):
    request_args = request.args.to_dict()
    if request.method == 'GET':
        return list_model(Img,request_args)
    elif request.method == 'DELETE':
        if 'admin' not in role_name:
            return '只有管理员或超级管理员可以删除图片'
        if request_args.get('id'):
            file_path = Img.query.filter_by(id=request_args.get('id'))[0].url
            file_delete(file_path)
        return delete_model(Img,db,request_args)
    else:
        return method_not_surpport_model()
 