from flask import Flask, request, jsonify, session
from library.extension import db
from flask_mysqldb import MySQL
from library.model import Role, Users
from library.total_price.controller import totals_data
from library.users.controller import users
from flask_jwt_extended import JWTManager
import random2
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_security import RoleMixin, SQLAlchemyUserDatastore, Security
import bcrypt
import eventlet
import eventlet.wsgi
import ssl
# from flask_apscheduler import APScheduler

from library.users.services import logout_inactive_users
# import memcache
# try:
#     # Kết nối đến Memcached server
#     memcached_client = memcache.Client(['127.0.0.1:11211'], debug=0)
#     print('ok')
# except Exception as e:
#     print(f"Đã xảy ra lỗi khi kết nối tới memcached: {e}")


app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nh2515901@gmail.com'
app.config['MAIL_PASSWORD'] = '841287775501aA'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

principal = Principal(app)
mail = Mail(app)
mysql = MySQL(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# scheduler = APScheduler()
# Cấu hình và khởi tạo APScheduler
# scheduler.init_app(app)
# scheduler.start()



socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chessdb_testupdate'
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['JWT_SECRET_KEY'] = 'my-jwt-secret-key'
login_manager = LoginManager()
login_manager.init_app(app)
admin_permission = Permission(RoleNeed('admin'))


user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
security = Security(app, user_datastore)
db.init_app(app)
with app.app_context():
    db.create_all()

    # Tạo vai trò admin nếu chưa tồn tại
    if not user_datastore.find_role('admin'):
        user_datastore.create_role(name='admin')

    db.session.commit()

    # Kiểm tra và tạo người dùng admin
    admin_user = Users.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        # Tạo người dùng mới và băm mật khẩu
        admin_password = '1'  # Mật khẩu ban đầu
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())
        admin_user = user_datastore.create_user(
            username='admin',
            email='admin@example.com',
            password=hashed_password,
            score=0,
            numMatch=0,
            is_admin=True
        )
        db.session.commit()

    # Gán vai trò admin cho người dùng admin
    admin_role = user_datastore.find_role('admin')
    if admin_user and admin_role:
        user_datastore.add_role_to_user(admin_user, admin_role)
        db.session.commit()

    db.session.commit()

    # Gán vai trò admin cho người dùng
    admin_role = user_datastore.find_role('admin')
    user_datastore.add_role_to_user(admin_user, admin_role)
    db.session.commit()

connected_clients = set()  # Initialize a set to store connected client IDs

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))
def create_app():
    return "APP created !"
@users.route('/')
def home():
    return 'Hello, HTTPS world!'

# scheduler.add_job(func=logout_inactive_users, trigger='interval', minutes=30)
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('mycert.crt', 'mykey.key')

# Tạo socket và bọc nó trong SSL context
listener = eventlet.listen(('0.0.0.0',0))
secure_listener = eventlet.wrap_ssl(listener, certfile='mycert.crt', keyfile='mykey.key', server_side=True)

# Chạy server

if __name__ == "__main__":
    app.register_blueprint(totals_data)
    app.register_blueprint(users)
    
    # Cấu hình và chạy server với SSL thông qua Flask-SocketIO
    socketio.run(app, debug=True, host='0.0.0.0', port=5001, keyfile='mykey.key', certfile='mycert.crt')
