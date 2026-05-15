import io
from utils.md_parser import to_html, to_txt
from flask_login import login_required, current_user
from flask import Blueprint, send_file, abort, session
from database.db_session import create_session
from database.notes import Note

export_bp = Blueprint('export_note', __name__, template_folder='templates')

def check_user(note_id):
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)

    if not note or note.user_id != current_user.id:
        db_sess.close()
        return None, None

    return note, db_sess

@export_bp.route('/note/<int:note_id>/export/md', methods=['GET'])
@login_required
def export_note_md(note_id):
    note, db_sess = check_user(note_id)
    if not note:
        abort(403)

    content = note.content.encode('utf-8')

    db_sess.close()
    return send_file(io.BytesIO(content), mimetype='text/plain', download_name=note.title + '.md', as_attachment=True)

@export_bp.route('/note/<int:note_id>/export/html', methods=['GET'])
@login_required
def export_note_html(note_id):
    note, db_sess = check_user(note_id)
    if not note:
        abort(403)

    body_html = to_html(note.content)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>""" + note.title + """</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
</head>
<body>
    <h1>""" + note.title + """</h1>
    """ + body_html + """
</body>
</html>"""

    db_sess.close()
    return send_file(io.BytesIO(html.encode('utf-8')), mimetype='text/html', download_name=note.title + '.html', as_attachment=True)

@export_bp.route('/note/<int:note_id>/export/txt', methods=['GET'])
@login_required
def export_note_txt(note_id):
    note, db_sess = check_user(note_id)
    if not note:
        abort(403)

    txt = to_txt(note.content)

    db_sess.close()
    return send_file(io.BytesIO(txt.encode('utf-8')), mimetype='text/plain', download_name=note.title + '.txt', as_attachment=True)
