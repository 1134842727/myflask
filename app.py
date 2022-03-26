from flask import Flask

app = Flask(__name__)

# database
from flask_sqlalchemy import SQLAlchemy
from config.db import DB_URI

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 将对应视图引用进来
from views.test_view import *

if __name__ == '__main__':
    app.run()
