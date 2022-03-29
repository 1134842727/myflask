from pip import main
from config.http_code import *
from flask import request,make_response
from utils.data_change import to_json
from utils.get_class_field import get_db_model_class_field
import pdb
def list_model(Model):
    model_list = []
    if 'id' in request.args:
        id = request.args['id']
        model = Model.query.filter_by(id=id)[0]
        model_list.append(to_json(model))
    else:
        models = Model.query.all()
        for model in models:
            model_list.append(to_json(model))
    response = make_response({"data": model_list, "code": SUCCESS_CODE})
    response.status = SUCCESS_CODE
    return response


def delete_model(Model,db):
    if 'id' in request.args:
        id = request.args['id']
        Model.query.filter_by(id=id).delete()
        db.session.commit()
        response = make_response()
        response.status = NO_CONTENT_CODE
        return response
    else:
        response = make_response({"message": '缺少id！', "code": BAD_REQUES_CODE})
        response.status = BAD_REQUES_CODE
        return response


def create_model(data,Model,db):
    field_list = get_db_model_class_field(Model)

    # 获取所有非空字段
    nullable_False_list = []
    for i in field_list:
        if hasattr(Model, i) and hasattr(getattr(Model,i),'nullable') and hasattr(getattr(Model,i),'primary_key'):
            if getattr(Model,i).nullable == False and getattr(Model,i).primary_key != True:
                nullable_False_list.append(i)
    # 判断所有非空字段是否都有值传入
    for i in nullable_False_list:
        if i not in data:
            response = make_response({"message": '{0}字段为必填！'.format(i), "code": BAD_REQUES_CODE})
            response.status = BAD_REQUES_CODE
            return response

    # 获取所有唯一字段
    unique_True_list = []
    for i in field_list:
        if hasattr(Model, i) and hasattr(getattr(Model,i),'unique'):
            if getattr(Model,i).unique == True:
                unique_True_list.append(i)
    # 所有唯一字段查询不能出现数据
    for i in unique_True_list:
        if Model.query.filter_by(**{i:data[i]}).count() > 0:
            response = make_response({"message": '{0}已存在！'.format(i), "code": CONFLICT_CODE})
            response.status = CONFLICT_CODE
            return response

    model = Model(**data)
    db.session.add(model)
    db.session.commit()
    response = make_response({"message": '新增成功！', "code": SUCCESS_CODE})
    response.status = SUCCESS_CODE
    return response

