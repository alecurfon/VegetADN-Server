from werkzeug.security import generate_password_hash, check_password_hash
import datetime, jwt

from .. import app, db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.password = generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def encode_auth_token(self):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id}
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class WhitelistToken(db.Model):
    __tablename__ = 'whitelist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    whitelisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.whitelisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_whitelist(auth_token):
        res = WhitelistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
