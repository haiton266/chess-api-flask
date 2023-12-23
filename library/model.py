from datetime import datetime
import uuid  # Sửa lỗi ở đây
from flask_security import RoleMixin
from library.extension import db
from flask_jwt_extended import get_jwt_identity
from flask_login import UserMixin
from flask_principal import Principal, Permission, RoleNeed

admin_role = RoleNeed('admin')
user_role = RoleNeed('user')

# Định nghĩa quyền dựa trên vai trò
admin_permission = Permission(admin_role)
user_permission = Permission(user_role, admin_role)
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)
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
                             )
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


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    numMatch = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=False)  # Thêm trường này
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    def __init__(self, username, password, email, score, numMatch, is_admin=False, active=False, roles=[], last_active=datetime.utcnow(),fs_uniquifier=None):  # Thêm tham số active (mặc định là False) và roles (mặc định là một mảng rỗng)
        self.username = username
        self.password = password
        self.email = email
        self.score = score
        self.numMatch = numMatch
        self.is_admin = is_admin
        self.active=active
        self.roles=roles
        self.last_active=last_active
        self.fs_uniquifier=fs_uniquifier# Cập nhật giá trị này
        if fs_uniquifier is None:
            fs_uniquifier = str(uuid.uuid4())
    def set_admin_status(self, admin_status):
        self.is_admin = admin_status

    def is_admin_user(self):
        return self.is_admin 
    

