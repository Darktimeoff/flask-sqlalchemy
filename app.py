from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from logging import basicConfig
from database import db, setup_database
from utils.main import get_env
from app.users.api import users_blueprint
from app.orders.api import orders_blueprint
from app.offers.api import offers_blueprint

basicConfig(filename='basic.log')
load_dotenv(override=True)


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = get_env('DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFACTIONS'] = False
    app.config['JSON_AS_ASCII'] = False

    db.init_app(app)
    Migrate(app, db, render_as_batch=True)

    return app

def register_urls(flask_app: Flask):
    flask_app.register_blueprint(users_blueprint)
    flask_app.register_blueprint(orders_blueprint)
    flask_app.register_blueprint(offers_blueprint)


app = create_app()
setup_database(app)
register_urls(app)

if __name__ == '__main__':
    app.run(debug=bool(get_env('DEBUG')))
