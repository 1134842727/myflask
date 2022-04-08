from app import db
class Img(db.Model):
    __tablename__ = 'img'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256),unique=True, nullable=False)
    description = db.Column(db.String(32), nullable=True)
   


