from library.extension import db
from flask_jwt_extended import get_jwt_identity

class Total_price(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chessBoard = db.Column(db.String(500),nullable = False)
    turn = db.Column(db.Integer)

    def __init__(self,chessBoard, turn):
        self. chessBoard= chessBoard
        self. turn= turn



