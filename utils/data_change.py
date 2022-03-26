def to_json(obj):
    """将实例对象转化为json"""
    item = obj.__dict__
    if "_sa_instance_state" in item:
        del item["_sa_instance_state"]
    return item