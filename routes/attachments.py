from flask import Blueprint, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import current_user, login_required
from database.db_session import create_session
from database.notes import Note
from database.attachments import Attachment
import os
import uuid
attachments_bp = Blueprint("attachments", __name__)
sup_extensions = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in sup_extensions


@attachments_bp.route("/note/<int:id>/attach", methods=["POST"])
@login_required
def upload_attachment(id):
    db_sess = create_session()
    note = db_sess.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        flash("Заметка не найдена", "danger")
        return redirect("/notes")

    files = request.files.getlist("files")
    if not files:
        flash("Файлы не выбраны", "danger")
        return redirect(request.referrer)

    for file in files:
        if file.filename == "":
            continue
        if not allowed_file(file.filename):
            flash("Недопустимый формат файла", "danger")
            continue
        ext = file.filename.rsplit(".", 1)[1]
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
        file.save(save_path)

        attachment = Attachment()
        attachment.filename = file.filename
        attachment.stored_name = unique_name
        attachment.file_type = ext
        attachment.note_id = note.id
        db_sess.add(attachment)
    db_sess.commit()
    flash("Файлы загружены", "success")
    return redirect(url_for("notes.edit_note", id=note.id))


@attachments_bp.route("/attachment/<int:id>")
@login_required
def get_attachment(id):
    db_sess = create_session()
    attachment = db_sess.query(Attachment).filter(Attachment.id == id).first()
    if not attachment:
        flash("Файл не найден", "danger")
        return redirect("/notes")
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], attachment.stored_name)


@attachments_bp.route("/attachment/<int:id>/delete", methods=["POST"])
@login_required
def delete_attachment(id):
    db_sess = create_session()
    attachment = db_sess.query(Attachment).filter(Attachment.id == id).first()
    if not attachment:
        flash("Файл не найден", "danger")
        return redirect("/notes")

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], attachment.stored_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    db_sess.delete(attachment)
    db_sess.commit()
    flash("Файл удалён", "success")
    return redirect(request.referrer)