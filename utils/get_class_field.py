def get_db_model_class_field(class_method):
    return [i for i in class_method.metadata.tables.items()][0][1].columns.keys()
