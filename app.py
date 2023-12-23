from flask import Flask, request, jsonify, session
from library.extension import db
from flask_mysqldb import MySQL
from library.model import Users
from library.total_price.controller import totals_data
from library.users.controller import users
from library.tournament.controller import tournament
from flask_jwt_extended import JWTManager
import eventlet
import random2
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta

# import memcache
# try:
#     # Kết nối đến Memcached server
#     memcached_client = memcache.Client(['127.0.0.1:11211'], debug=0)
#     print('ok')
# except Exception as e:
#     print(f"Đã xảy ra lỗi khi kết nối tới memcached: {e}")


app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nh2515901@gmail.com'
app.config['MAIL_PASSWORD'] = '841287775501aA'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
mysql = MySQL(app)
jwt = JWTManager(app)
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/chessdb_testupdate'
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['JWT_SECRET_KEY'] = 'my-jwt-secret-key'


db.init_app(app)
with app.app_context():
    db.create_all()
    print("Created DB")

connected_clients = set()  # Initialize a set to store connected client IDs


def create_app():
    return "APP created !"


# @socketio.on("connect")
# def connected():
#     global connected_clients
#     client_id = request.sid
#     global old_time
#     old_time = datetime.now()
#     if client_id not in connected_clients:
#         connected_clients.add(client_id)
#         print(client_id)
#         print("client has connected")
#         emit("connect", {"data": f"id: {client_id} is connected"})


# @socketio.on("disconnect")
# def disconnected():
#     global connected_clients
#     client_id = request.sid
#     if client_id in connected_clients:
#         connected_clients.remove(client_id)
#         print("user disconnected")
#         emit("disconnect", f"user {client_id} disconnected", broadcast=True)


# @socketio.on('get_time')
# def send_time_interval():
#     print("TIME START COUNTING")
#     global old_time

#     while True:
#         # Calculate the time difference
#         time_diff = datetime.now() - old_time

#         # Remove milliseconds from the time difference
#         time_diff_without_ms = time_diff - \
#             timedelta(microseconds=time_diff.microseconds)
#         time_diff_without_ms = 20 - time_diff_without_ms.seconds
#         if time_diff_without_ms <= 0:
#             time_diff_without_ms = 0
#         # Xử lý thằng thắng thằng thua
#         # Change timedelta to string for JSON serialization
#         emit("get_time", {"time": str(time_diff_without_ms)})
#         eventlet.sleep(0.25)


# if __name__ == "__main__":
#     app.register_blueprint(totals_data)
#     app.register_blueprint(users)
#     app.run(debug=True)
#     # socketio.run(app, debug=True, port=5000)


if __name__ == "__main__":
    app.register_blueprint(totals_data)
    app.register_blueprint(users)
    app.register_blueprint(tournament)
    # Remove app.run(debug=True)
    # Run the application using SocketIO
    socketio.run(app, debug=True, port=5001)
