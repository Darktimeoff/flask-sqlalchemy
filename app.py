from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from logging import basicConfig
from database import db, setup_database
from utils.main import get_env

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


app = create_app()
setup_database(app)

if __name__ == '__main__':
    app.run(debug=bool(get_env('DEBUG')))
