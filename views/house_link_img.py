
import pdb
from flask import request
from config.http_code import *
from app import app,db
from models.house_link_img import House_link_img
from views.base_view import list_model,delete_model,patch_model,method_not_surpport_model,create_model_simple
from views.user import certification
@app.route('/house_link_img',methods=['GET','POST','DELETE','PATCH'])
@certification
def house_link_img(username,role_name):
    data = request.json
    request_args_dict = request.form.to_dict()
    if request.method == 'GET':
        return list_model(House_link_img,request_args_dict)
    elif request.method == 'POST': 
        if 'admin' not in role_name:
            return '只有管理员可用！'
        if 'hid' not in data:
            return '缺少hid字段，为房屋id'
        if 'iid' not in data:
            return '缺少iid字段，为图片id列表'
        house_link_img_data = list_model(House_link_img,request_args_dict).json.get('data')
        for img_id in data.get('iid'):
            post_data = {'hid':data.get('hid'),'iid':img_id}
            if post_data in house_link_img_data:
                return '已存在关系{0}'.format(post_data) 
        for img_id in data.get('iid'):
            post_data = {'hid':data.get('hid'),'iid':img_id}
            create_model_simple(House_link_img,post_data,db)
        return '房屋图片关联成功！'
    elif request.method == 'PATCH':
        if 'admin' not in role_name:
            return '只有管理员可用！'
        return patch_model(House_link_img,data,request_args_dict,db)
    elif request.method == 'DELETE':
        if 'admin' not in role_name:
            return '只有管理员可用！'
        house = list_model(House_link_img,request_args_dict)
        if house.json.get('data'):
            if len(house.json.get('data')) != 1:
                return '符合条件的数据非一条，请检查筛选条件！'
        return delete_model(House_link_img,db,request_args_dict)
    else:
        return method_not_surpport_model()