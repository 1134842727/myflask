
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.img import Img
from models.house_link_img import House_link_img
from views.base_view import create_model, list_model,delete_model,method_not_surpport_model,create_model_simple
from utils.file_manager import file_delete,file_upload
from views.user import certification
import pdb
@app.route('/img',methods=['GET','DELETE','POST'])
@certification
def img(username,role_name):
    img_id_list = []
    data = request.form.to_dict()
    request_args = request.args.to_dict()
    if request.method == 'GET':
        return list_model(Img,request_args)
    elif request.method == 'POST':
        if 'admin' not in role_name:
            return '只有管理员或超级管理员可以添加图片'
        files = request.files.getlist('img')
        if files:
            for file in files:
                file_url = file_upload(file)
                img = Img(url=file_url,description=data.get('description'))
                db.session.add(img)
                db.session.commit()
                img_id_list.append(img.id)
                response = make_response({"data": img_id_list, "code": SUCCESS_CODE})
                response.status = SUCCESS_CODE
        else:
                response = make_response({"data": '表单img为空', "code": BAD_REQUES_CODE})
                response.status = BAD_REQUES_CODE
        return response
    elif request.method == 'DELETE':
        if 'admin' not in role_name:
            return '只有管理员或超级管理员可以删除图片'
        if request_args.get('id'):
            file_path = Img.query.filter_by(id=request_args.get('id'))[0].url
            file_delete(file_path)
        return delete_model(Img,db,request_args)
    else:
        return method_not_surpport_model()
 