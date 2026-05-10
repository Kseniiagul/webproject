from flask import Flask
from database import db_session

app = Flask(__name__)


def main():
    db_session.global_init("db/notes.db")
    app.run()


if __name__ == '__main__':
    main()
