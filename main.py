from database import db_session
from flask import Flask
from routes.auth import authorization_routes
from routes.export import export_note
from routes.view import view_note
from routes.api import api_note

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our-secret-key-here'

authorization_routes(app)


def main():
    db_session.global_init("db/notes.db")

    app.register_blueprint(export_note)
    app.register_blueprint(view_note)
    app.register_blueprint(api_note)

    app.run()


if __name__ == '__main__':
    main()
