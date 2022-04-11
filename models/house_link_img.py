from app import db
class House_link_img(db.Model):
    __tablename__ = 'house_link_img'
    hid = db.Column(db.Integer, db.ForeignKey('house.id'),primary_key=True)
    iid = db.Column(db.Integer, db.ForeignKey('img.id'),primary_key=True)

