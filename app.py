from flask import Flask
from routes.auth import authorization_routes
from routes.notes import notes_bp
from routes.attachments import attachments_bp
from routes.api import api_bp
from routes.export import export_bp
from routes.view import view_bp
from database.db_session import global_init
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

global_init("db/notes.db")
authorization_routes(app)
app.register_blueprint(notes_bp)
app.register_blueprint(attachments_bp)
app.register_blueprint(api_bp)
app.register_blueprint(export_bp)
app.register_blueprint(view_bp)