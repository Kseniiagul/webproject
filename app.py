from flask import Flask
from flask_login import LoginManager
from routes.auth import authorization_routes
from routes.notes import notes_bp
from routes.attachments import attachments_bp
from routes.api import api_bp
from routes.export import export_bp

# from routes.view import view_bp - у меня такой вариант импорта не работает
from routes.view import blueprint as view_bp

from database.db_session import global_init
from database.users import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

global_init("db/notes.db")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    from database.db_session import create_session
    db_sess = create_session()
    return db_sess.get(User, int(user_id))


@app.route('/')
def index():
    from flask import redirect, url_for
    return redirect(url_for('login'))


authorization_routes(app)
app.register_blueprint(notes_bp)
app.register_blueprint(attachments_bp)
app.register_blueprint(api_bp)
app.register_blueprint(export_bp)
app.register_blueprint(view_bp)

if __name__ == '__main__':
    app.run(debug=True)
