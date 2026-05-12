from database import db_session
from flask import Flask
from database.notes import Note
from routes.auth import authorization_routes
from routes.export import export_note
from routes.view import view_note
from routes.api import api_note

app = Flask(__name__)
app.config['SECRET_KEY'] = 'our-secret-key-here'

authorization_routes(app)


def main():
    db_session.global_init("db/notes.db")

    # подобным образом заполнялись и остальные поля в базе данных
    # note = Note()
    # note.title = "Покупки"
    # note.content = "Творог, бананы, мука, молоко, чай."
    # note.user_id = 1
    # db_sess = db_session.create_session()
    # db_sess.add(note)
    # db_sess.commit()

    app.register_blueprint(export_note)
    app.register_blueprint(view_note)
    app.register_blueprint(api_note)

    app.run()


if __name__ == '__main__':
    main()
