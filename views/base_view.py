
from config.http_code import *
from flask import request,make_response
from utils.data_change import to_json
from utils.get_class_field import get_db_model_class_field
import pdb


def list_model(Model,params,hide_key_list=None):
    model_list = []
    if params:
        models = Model.query.filter_by(**params)
        if models.count() > 0:
            for model in models:
                model_list.append(to_json(model))
    else:
        models = Model.query.all()
        for model in models:
            data = to_json(model)
            if hide_key_list:
                for hide_key in hide_key_list:
                    del data[hide_key]
            model_list.append(to_json(model))
    response = make_response({"data": model_list, "code": SUCCESS_CODE})
    response.status = SUCCESS_CODE
    return response


def delete_model(Model,db,params):
    if params:
        # 保证删除的参数存在，防止异常
        for i in params:
            if not hasattr(Model, i):
                response = make_response({"message": '没有{0}参数！'.format(i), "code": BAD_REQUES_CODE})
                response.status = BAD_REQUES_CODE
                return response
        Model.query.filter_by(**params).delete()
        db.session.commit()
        response = make_response()
        response.status = NO_CONTENT_CODE
        return response
    else:
        response = make_response({"message": '缺少params！', "code": BAD_REQUES_CODE})
        response.status = BAD_REQUES_CODE
        return response


def create_model(Model,data,db):
    field_list = get_db_model_class_field(Model)

    # 保证创建的字段存在且数据类型是否正确，防止异常
    for i in data:
        if not hasattr(Model, i):
            response = make_response({"message": '没有{0}参数！'.format(i), "code": BAD_REQUES_CODE})
            response.status = BAD_REQUES_CODE
            return response
        if getattr(Model,i).type.python_type != type(data[i]):
            response = make_response({"message": '{0}预期为{1}类型，实际为{2}类型！'.format(i,getattr(Model,i).type.python_type,type(data[i])), "code": BAD_REQUES_CODE})
            response.status = BAD_REQUES_CODE
            return response

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

def patch_model(Model,data,params,db):
    field_list = get_db_model_class_field(Model)

    # 保证修改的字段存在且数据类型是否正确，防止异常
    for i in data:
        if not hasattr(Model, i):
            response = make_response({"message": '没有{0}参数！'.format(i), "code": BAD_REQUES_CODE})
            response.status = BAD_REQUES_CODE
            return response
        if getattr(Model,i).type.python_type != type(data[i]):
            response = make_response({"message": '{0}预期为{1}类型，实际为{2}类型！'.format(i,getattr(Model,i).type.python_type,type(data[i])), "code": BAD_REQUES_CODE})
            response.status = BAD_REQUES_CODE
            return response

    # 获取所有唯一字段
    unique_True_list = []
    for i in field_list:
        if hasattr(Model, i) and hasattr(getattr(Model,i),'unique'):
            if getattr(Model,i).unique == True:
                unique_True_list.append(i)
    # 修改字段如果是唯一字段则不能跟原来数据库重复
    for i in data:
        if i in unique_True_list and Model.query.filter_by(**{i:data[i]}).count() > 0:
            response = make_response({"message": '{0}已存在！'.format(i), "code": CONFLICT_CODE})
            response.status = CONFLICT_CODE
            return response

    model = Model.query.filter_by(**params)
    if model.count() > 1:
        response = make_response({"message": '满足条件的数据不止一条，请确认筛选参数', "code": CONFLICT_CODE})
        response.status = BAD_REQUES_CODE
        return response
    elif model.count() == 1:
        model = model[0]
    else:
        response = make_response({"message": '没有符合条件的数据，请确认筛选参数', "code": NOT_FOUND_CODE})
        response.status = NOT_FOUND_CODE
        return response
    for i in data:
        setattr(model,i,data[i]) 

    db.session.commit()
    response = make_response()
    response.status = NO_CONTENT_CODE
    return response


def method_not_surpport_model():
    response = make_response({"message": '请求的方法不支持!', "code": BAD_REQUES_CODE})
    response.status = BAD_REQUES_CODE
    return response
