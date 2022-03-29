from flask import Flask

app = Flask(__name__)

# database
from flask_sqlalchemy import SQLAlchemy
from config.db import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 将对应视图引用进来
from views.role import *
from views.user import *
if __name__ == '__main__':
    # 本地调试
    app.run(debug=True,host='127.0.0.1',port=5000)
    # 对外暴露
    # app.run(debug=True,host='0.0.0.0',port=5000)
