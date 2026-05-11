import io
from utils.md_parser import to_html, to_txt
from Flask import Blueprint, send_file, abort, session
from database import create_session
from database.notes import Note

blueprint = Blueprint('export_note', __name__, templates_folder='templates')

def check_user(note_id):
    if 'user_id' not in session:
        return None
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)
    db_sess.close()

    if not note or note.user_id != session['user_id']:
        return None

    return note

@blueprint.route('/note/<int:note_id>/export/md', methods=['GET'])
def export_note_md(note_id):
    note = check_user(note_id)
    if not note:
        abort(403)

    content = note.content.encode('utf-8')

    return send_file(io.BytesIO(content), mimetype='text/plain', download_name=note.title + '.md', as_attachment=True)

@blueprint.route('/note/<int:note_id>/export/html', methods=['GET'])
def export_note_html(note_id):
    note = check_user(note_id)
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
<h1>""" + note.title + """</h1>
<body>""" + body_html + """</body>
</html>"""

    return send_file(io.BytesIO(html.encode('utf-8')), mimetype='text/html', download_name=note.title + '.html', as_attachement=True)

@blueprint.route('/note/<int:note_id>/export/txt', methods=['GET'])
def export_note_txt(note_id):
    note = check_user(note_id)
    if not note:
        abort(403)

    txt = to_txt(note.content)

    return send_file(io.BytesIO(txt.encode('utf-8')), mimetype='text/plain', download_name=note.title + '.txt', as_attachment=True)





