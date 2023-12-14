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
    # ... các trường khác ...
    time_player1 = db.Column(db.Integer, nullable=False,
                             )  # 900 giây = 15 phút
    time_player2 = db.Column(db.Integer, nullable=False)

    def __init__(self, chessBoard, turn, codeGame, player1, player2, winner, time_player1, time_player2):
        self. chessBoard = chessBoard
        self. turn = turn
        self.codeGame = codeGame
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.time_player1 = time_player1
        self.time_player2 = time_player2


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    numMatch = db.Column(db.Integer, nullable=False)

    def __init__(self, username, password, email, score, numMatch):
        self.username = username
        self.password = password
        self.email = email
        self.score = score
        self.numMatch = numMatch


# class UserRegistrationTemp(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     hashed_password = db.Column(db.String(200), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     otp = db.Column(db.String(6), nullable=False)
#     expires_at = db.Column(db.DateTime, nullable=False)
