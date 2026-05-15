from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from database.notes import Note
from database.attachments import Attachment
from database.db_session import create_session
from utils.md_parser import to_html

blueprint = Blueprint('view_note', __name__, template_folder='templates')


@blueprint.route('/note/<int:note_id>', methods=['GET'])
@login_required
def view_note(note_id):
    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)
    if not note or note.user_id != current_user.id:
        db_sess.close()
        abort(404)

    rendered_html = to_html(note.content)

    attachments = db_sess.query(Attachment).filter(Attachment.note_id == note_id).all()

    db_sess.close()

    return render_template('note_view.html', note=note, rendered_html=rendered_html, attachments=attachments)
