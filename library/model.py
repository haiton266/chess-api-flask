from library.extension import db
from flask_jwt_extended import get_jwt_identity


class Total_price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chessBoard = db.Column(db.String(500), nullable=False)
    turn = db.Column(db.Integer)
    codeGame = db.Column(db.String(50), nullable=False)
    player1 = db.Column(db.String(50), nullable=False)
    player2 = db.Column(db.String(50), nullable=False)
    winner = db.Column(db.String(50), nullable=False)

    def __init__(self, chessBoard, turn, codeGame, player1, player2, winner):
        self. chessBoard = chessBoard
        self. turn = turn
        self.codeGame = codeGame
        self.player1 = player1
        self.player2 = player2
        self.winner = winner


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, score):
        self.username = username
        self.password = password
        self.score = score
