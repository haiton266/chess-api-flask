from flask_sqlalchemy import SQLAlchemy
from library.extension import db
from flask_jwt_extended import get_jwt_identity


class Round(db.Model):
    __tablename__ = 'rounds'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    seeds = db.relationship('Seed', backref='round', lazy=True)

    def __init__(self, title):
        self.title = title


class Seed(db.Model):
    __tablename__ = 'seeds'
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey(
        'rounds.id'), nullable=False)
    matchID = db.Column(db.String(100))
    result = db.Column(db.String(50))
    teams = db.relationship('Team', backref='seed', lazy=True)

    def __init__(self, round_id, matchID, result):
        self.round_id = round_id
        self.matchID = matchID
        self.result = result


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    seed_id = db.Column(db.Integer, db.ForeignKey('seeds.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, seed_id, name):
        self.seed_id = seed_id
        self.name = name


class Total_price(db.Model):  # Chessboard
    id = db.Column(db.Integer, primary_key=True)
    chessBoard = db.Column(db.String(500), nullable=False)
    turn = db.Column(db.Integer)
    codeGame = db.Column(db.String(50), nullable=False)
    player1 = db.Column(db.String(50), nullable=False)
    player2 = db.Column(db.String(50), nullable=False)
    winner = db.Column(db.String(50), nullable=False)
    time_player1 = db.Column(db.Integer, nullable=False)
    time_player2 = db.Column(db.Integer, nullable=False)
    total_time1 = db.Column(db.Integer, nullable=False)
    total_time2 = db.Column(db.Integer, nullable=False)

    def __init__(self, chessBoard, turn, codeGame, player1, player2, winner, time_player1, time_player2):
        self. chessBoard = chessBoard
        self. turn = turn
        self.codeGame = codeGame
        self.player1 = player1
        self.player2 = player2
        self.winner = winner
        self.time_player1 = time_player1
        self.time_player2 = time_player2
        self.total_time1 = 300
        self.total_time2 = 300


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
