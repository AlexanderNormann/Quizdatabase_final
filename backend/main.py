import os

from models.database import create_database
from flask import Flask
from controllers.controller import routes_blueprint


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

    app.register_blueprint(routes_blueprint)

    return app


app = create_app()

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
