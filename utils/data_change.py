import pdb
import copy
def to_json(obj):
    """将实例对象转化为json"""
    item1 = obj.__dict__
    if "_sa_instance_state" in item1:
        
        del item1["_sa_instance_state"]
    
    # item2 = copy.deepcopy(item1)
    # for i in item2:
    #     if "_sa_instance_state" in dir(item2[i]):
    #         del item2[i].__dict__["_sa_instance_state"]
    #         item1[i] = item2[i].__dict__
    return item1