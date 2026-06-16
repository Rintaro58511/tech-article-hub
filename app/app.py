from flask import Flask
from model import db, User
from flask_login import LoginManager
from flask_migrate import Migrate
from main.views import main_bp
from auth.views import auth_bp

app = Flask(__name__)

app.config.from_object("config.Config")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(int(user_id))

db.init_app(app)
Migrate(app, db)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)