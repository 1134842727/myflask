from flask import Flask
from config.media import MEDIA_ROOT
import pdb
app = Flask(__name__)
app.config['MEDIA_ROOT'] = MEDIA_ROOT

# database
from flask_sqlalchemy import SQLAlchemy
from config.db import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 将对应视图引用进来
from views.role import *
from views.user import *
from views.img import *
from views.house import *
from views.house_link_img import *
#没有视图的模型需要单独引入，因为需要相关db处理代码
# 如：from models.img import Img
if __name__ == '__main__':
    # 本地调试
    app.run(debug=True,host='127.0.0.1',port=5000)
    # 对外暴露
    # app.run(debug=True,host='0.0.0.0',port=5000)
