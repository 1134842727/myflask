
import pymysql
pymysql.install_as_MySQLdb()
DIALECT = 'mysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test'
#mysql 不会认识utf-8,而需要直接写成utf8
DB_URI = "mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8".format( USERNAME, PASSWORD, HOST, PORT, DATABASE)