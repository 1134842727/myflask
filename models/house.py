from app import db
class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32),nullable=False)
    cover = db.Column(db.Integer,db.ForeignKey('img.id'),nullable=True)
    remark = db.Column(db.String(256),nullable=True)
    if_show = db.Column(db.Boolean,nullable=False)
    house_type = db.Column(db.String(16),nullable=True)
    price = db.Column(db.Integer,nullable=False)
    size = db.Column(db.Integer,nullable=False)

