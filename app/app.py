from flask import Flask
from main.model import db
from main.views import main_bp


app = Flask(__name__)

app.config.from_object("config.Config")

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)