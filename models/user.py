from app import db
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16),nullable=True)
    username = db.Column(db.String(16),unique=True, nullable=False)
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))



