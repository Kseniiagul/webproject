import datetime
from flask import Blueprint, abort, session, jsonify, request
from database.notes import Note
from database.attachments import Attachment
from database.db_session import create_session

blueprint = Blueprint('api_note', __name__, template_folder='templates')

@blueprint.route('/api/notes', methods=['GET'])
def api_notes():
    if 'user_id' not in session:
        abort(401)
    db_sess = create_session()
    notes = db_sess.query(Note).filter(Note.user_id == session['user_id']).order_by(Note.updated_at.desc()).all()

    results = []
    for note in notes:
        note_ = {
            'id': note.id,
            'title': note.title,
            'updated_at': note.updated_at
        }
        results.append(note_)

    db_sess.close()

    return jsonify(results)

@blueprint.route('/api/note/<int:id>', methods=['GET'])
def api_note(note_id):
    if 'user_id' not in session:
        abort(401)
    db_sess = create_session()

    note = db_sess.query(Note).get(note_id)
    if not note or note.user_id != session['user_id']:
        db_sess.close()
        abort(404)

    attachments_ = []
    attachments = db_sess.query(Attachment).filter(Attachment.note_id == note_id).all()
    for attachment in attachments:
        attachment_ = {
            'id': attachment.id,
            'filename': attachment.filename,
            'stored_name': attachment.stored_name,
            'file_type': attachment.file_type
        }
        attachments_.append(attachment_)

    result = {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at,
        'updated_at': note.updated_at,
        'user_id': note.user_id,
        'attachments': attachments_,
    }

    db_sess.close()

    return jsonify(result)

@blueprint.route('/api/note', methods=['POST'])
def api_note_post():
    if 'user_id' not in session:
        abort(401)

    data = request.get_json()
    if not data or 'title' not in data:
        abort(400)

    db_sess = create_session()
    note = Note(
        title = data['title'],
        content = data.get('content', ''),
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now(),
        user_id = session['user_id']
    )

    db_sess.add(note)
    db_sess.commit()
    note_id = note.id
    db_sess.close()

    return jsonify({'id': note_id, 'message': 'created'}), 201

@blueprint.route('/api/note/<int:id>', methods=['PUT'])
def api_note_update(note_id):
    if 'user_id' not in session:
        abort(401)

    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)

    if not note or note.user_id != session['user_id']:
        db_sess.close()
        abort(404)

    data = request.get_json()
    if not data:
        db_sess.close()
        abort(400)

    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    note.updated_at = datetime.datetime.now()

    db_sess.commit()
    db_sess.close()

    return jsonify({'id': note_id, 'message': 'updated'})

@blueprint.route('/api/note/<int:id>', methods=['DELETE'])
def api_note_delete(note_id):
    if 'user_id' not in session:
        abort(401)

    db_sess = create_session()
    note = db_sess.query(Note).get(note_id)

    if not note or note.user_id != session['user_id']:
        db_sess.close()
        abort(404)

    db_sess.delete(note)
    db_sess.commit()
    db_sess.close()

    return jsonify({'id': note_id, 'message': 'deleted'})
