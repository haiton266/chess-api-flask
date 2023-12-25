import datetime
import memcache

import bcrypt
from flask_mail import Mail
from flask_mail import Message
import random2
from flask import Flask
from library.extension import db
from library.library_ma import UserSchema
from flask import request, jsonify, json, session
from library.model import  Users
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt, unset_jwt_cookies
users_schema = UserSchema(many=True)
user_schema = UserSchema()
from flask_principal import identity_changed, Identity
from flask_principal import RoleNeed,Permission,AnonymousIdentity
from flask import current_app
try:
    memcached_client = memcache.Client(['127.0.0.1:11211'], debug=0)

except Exception as e:
    print(f"Đã xảy ra lỗi khi kết nối tới memcached: {e}")

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nh2515901@gmail.com'
app.config['MAIL_PASSWORD'] = 'hvyz kumj acbn qrni'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
admin_role = RoleNeed('admin')
user_role = RoleNeed('user')
admin_permission = Permission(admin_role)


def create_token(user_id):
    expires = datetime.timedelta(minutes=30)
    access_token = create_access_token(identity=user_id, expires_delta=expires)
    return access_token

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin_panel():
    return 'Chỉ dành cho quản trị viên!'


def get_all_users_status_service():
    users = Users.query.all()
    users_status = [{"username": user.username, "active": user.active} for user in users]
    return jsonify(users_status)





def verify_otp():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']
    user_otp = data['otp']
    stored_otp = memcached_client.get(f"username:{username}")
    try:
        # Kiểm tra xem OTP đã được sử dụng để tạo tài khoản hay chưa
        if stored_otp and int(stored_otp) == int(user_otp) and not memcached_client.get(f"otp_used:{user_otp}"):
            hashed_password = hash_password(password)
            new_user = Users(username=username, password=hashed_password, email=email, score=0, numMatch=0)
            db.session.add(new_user)
            db.session.commit()
            # Đánh dấu mã OTP đã được sử dụng
            memcached_client.set(f"otp_used:{user_otp}", 'used', time=3600)  # Giả sử mã OTP sẽ hết hạn sau 1 giờ
            print("ök4")
            return jsonify({'message': 'OTP verified successfully'}), 200
        else:
            return jsonify({'message': 'Invalid OTP or OTP already used'}), 400
    except Exception as e:
        return jsonify({'message': 'Error at try catch'}), 400


def send_otp(email):
    try:
        otp = random2.randint(100000, 999999)
        msg = Message('Your OTP', sender='nh2515901@gmail.com',
                      recipients=[email])
        msg.body = f'Your OTP is {otp}'
        mail.send(msg)
        return otp, True
    except Exception as e:
        print("Error sending email: ", str(e))
        return None, False




def load_user(user_id):
    # Lấy thông tin người dùng từ database
    return Users.get(user_id)

def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    # Kiểm tra dữ liệu đầu vào
    if not username or not password or not email:
        return {'message': 'Username, password and email are required'}, 400

    # Kiểm tra xem người dùng đã tồn tại chưa
    user = Users.query.filter_by(username=username).first()
    if user:
        return {'message': 'Username already exists'}, 400

    # Gửi OTP qua email
    otp, otp_sent = send_otp(email)
    if not otp_sent:
        # Thông báo không gửi được OTP
        return {'message': 'Failed to send OTP. Please check the email address and try again.'}, 500

    memcached_client.set(f"username:{username}", otp, time=300)

    # Lưu OTP vào session hoặc cơ sở dữ liệu
    # session['otp'] = otp

    # Tạo người dùng mới
    # hashed_password = generate_password_hash(password)
    # new_user = Users(username=username, password=hashed_password,
    #                  email=email, score=0, numMatch=0)
    # db.session.add(new_user)
    # db.session.commit()

    # Thông báo OTP đã được gửi thành công
    return {'message': 'OTP sent to email successfully. Please verify.'}


# def check_password(hashed_password, password):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return {'message': 'Username and password are required'}, 400

    user = Users.query.filter_by(username=username).first()

    if not user:
        return {'message': 'Invalid username or password'}, 401

    password_encoded = password.encode('utf-8')
    stored_password = user.password if isinstance(user.password, bytes) else user.password.encode('utf-8')

    if bcrypt.checkpw(password_encoded, stored_password):
        identity = Identity(user.id)
        user.active = True
        db.session.commit()
        if user.is_admin:
            identity.provides.add(admin_role)
        else:
            identity.provides.add(user_role)

        identity_changed.send(current_app._get_current_object(), identity=identity)

        login_method = data.get('login_method', 'token')

        if login_method == 'token':
            access_token = create_access_token(identity=user.id)
            return {'username': user.username, 'id': user.id, 'score': user.score, 'access_token': access_token}, 200
        elif login_method == 'session':
            session['id'] = user.id
            session['username'] = user.username
            return {'message': f'{user.username} Login success'}, 200
        else:
            return {'message': 'Invalid login method'}, 400
    else:
        return {'message': 'Invalid username or password'}, 401


def logout(username):
    # Tìm người dùng dựa trên username
    user = Users.query.filter_by(username=username).first()
    if user:
        user.active = False
        db.session.commit()

        # Xóa thông tin người dùng khỏi session
        session.pop('username', None)
        session.pop('id', None)

        print(f"User {username} logged out")
        return jsonify({'message': f'{username} logged out successfully'})
    else:
        return jsonify({'message': 'User not found'})

def update_last_active(user_id):
    user = Users.query.get(user_id)
    if user:
        user.last_active = datetime.utcnow()
        db.session.commit()



def logout_inactive_users():
    # Đặt thời gian không hoạt động tối đa, ví dụ: 30 phút
    max_inactive_time = datetime.timedelta(minutes=30)

    # Tìm tất cả người dùng không hoạt động quá thời gian cho phép
    inactive_users = Users.query.filter(
        Users.last_active < (datetime.utcnow() - max_inactive_time)
    ).all()

    for user in inactive_users:
        user.active = False
        # Thêm bất kỳ logic đăng xuất nào khác ở đây
        db.session.commit()

def get_all_users_service():
    users = Users.query.all()
    if users:
        return users_schema.jsonify(users)
    else:
        return jsonify({"message": "Not found users!"})


def get_user_by_id_service(id):
    user = Users.query.get(id)
    if user:
        return user_schema.jsonify(user)
    else:
        return jsonify({"message": "Not found user"}),


def update_user_by_id_service(id):
    user = Users.query.get(id)
    data = request.json
    if user:
        if data and "password" in data and "username" in data:
            try:
                user.username = data["username"]
                user.password = data["password"]
                user.score = data["score"]
                user.numMatch = data["numMatch"]
                db.session.commit()
                return "user Updated"
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not delete book!"}), 400
    else:
        return "Not found user"


def update_user_by_username_service(username):
    user = Users.query.filter_by(username=username).first()
    data = request.json
    if user:
        if data and "score" in data:
            try:
                user.score += data["score"]
                user.numMatch += 1
                db.session.commit()
                return "user Updated"
            except IndentationError:
                db.session.rollback()
                return jsonify({"message": "Can not update!"}), 400
        else:
            return jsonify({"message": "Invalid input data"}), 400
    else:
        return "Not found user"


def delete_User_data_by_id_service(id):
    price = Users.query.get(id)
    if price:
        try:
            db.session.delete(price)
            db.session.commit()
            return jsonify({"message": "User deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot delete User!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Not found User!"}), 404
