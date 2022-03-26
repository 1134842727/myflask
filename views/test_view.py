
import sqlalchemy
from flask import request,make_response
from config.http_code import *
from app import app,db
from models.test_model import Test_model
from utils.data_change import to_json

@app.route('/test/model',methods=['GET','POST','DELETE','PATCH'])
def test_model():
    if request.method == 'GET':
        role_list = []
        if 'id' in request.args:
            id = request.args['id']
            role = Test_model.query.filter_by(id=id)[0]
            role_list.append(to_json(role))
        else:
            roles = Test_model.query.all()
            for role in roles:
                role_list.append(to_json(role))
        response = make_response({"data": role_list, "code": SUCCESS_CODE})
        response.status = SUCCESS_CODE
        return response
    elif request.method == 'PATCH':
        if request.json.get('name') == None or 'id' not in request.args:
            return 'name或id不能为空'
        id = request.args['id']
        try:
            role = Test_model.query.filter_by(id=id)[0]
        except IndexError as e:
            response = make_response({"message": 'id不存在！', "code": NOT_FOUND_CODE})
            response.status = NOT_FOUND_CODE
            return response
        try:
            role = Test_model.query.filter_by(name=request.json.get('name'))[0]
            response = make_response({"message": 'name已存在！', "code": CONFLICT_CODE})
            response.status = NOT_FOUND_CODE
            return response
        except IndexError as e:
            role.name = request.json.get('name')
            db.session.commit()
            response = make_response()
            response.status = NO_CONTENT_CODE
            return response
    elif request.method == 'POST':
        try:
            data = request.json
            if data.get('name') == None:
                return '名称不能为空'
            try:
                role = Test_model.query.filter_by(name=data.get('name'))[0]
                response = make_response({"message": '名称已存在！', "code": CONFLICT_CODE})
                response.status = CONFLICT_CODE
                return response
            except IndexError as e:
                role = Test_model(name=data.get('name'))
                db.session.add(role)
                db.session.commit()
                response = make_response({"message": '新增成功！', "code": SUCCESS_CODE})
                response.status = SUCCESS_CODE
                return response
        except sqlalchemy.exc.IntegrityError as e:
            message = str(e.args[0])
            response = make_response({"message": message, "code": CONFLICT_CODE})
            response.status = CONFLICT_CODE
            return response
    elif request.method == 'DELETE':
        if 'id' in request.args:
            id = request.args['id']
            Test_model.query.filter_by(id=id).delete()
            db.session.commit()
            response = make_response()
            response.status = NO_CONTENT_CODE
            return response
        else:
            response = make_response({"message": '缺少id！', "code": BAD_REQUES_CODE})
            response.status = BAD_REQUES_CODE
            return response
    else:
        response = make_response({"message": '请求的方法不支持', "code": BAD_REQUES_CODE})
        response.status = BAD_REQUES_CODE
        return response
