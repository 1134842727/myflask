import pdb
import sqlalchemy
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.user import User
from utils.data_change import to_json
from views.base_view import list_model,delete_model,create_model
@app.route('/user',methods=['GET','POST','DELETE','PATCH'])
def user():
    if request.method == 'GET':
        return list_model(User,request.args.to_dict())
    elif request.method == 'PATCH':
        if request.json.get('name') == None or 'id' not in request.args:
            return 'name或id不能为空'
        id = request.args['id']
        try:
            user = User.query.filter_by(id=id)[0]
        except IndexError as e:
            response = make_response({"message": 'id不存在！', "code": NOT_FOUND_CODE})
            response.status = NOT_FOUND_CODE
            return response
        try:
            user = User.query.filter_by(username=request.json.get('username'))[0]
            response = make_response({"message": 'username已存在！', "code": CONFLICT_CODE})
            response.status = NOT_FOUND_CODE
            return response
        except IndexError as e:
            user.username = request.json.get('username')
            user.role_id = 1
            db.session.commit()
            response = make_response()
            response.status = NO_CONTENT_CODE
            return response
    elif request.method == 'POST':
        data = request.json
        return create_model(data,User,db)
    elif request.method == 'DELETE':
        return delete_model(User,db,request.args.to_dict())
    else:
        response = make_response({"message": '请求的方法不支持', "code": BAD_REQUES_CODE})
        response.status = BAD_REQUES_CODE
        return response
