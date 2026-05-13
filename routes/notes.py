from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
from flask_login import current_user, login_required
from database.db_session import create_session
from database.notes import Note
notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes")
@login_required
def notes_list():
    db_sess = create_session()
    notes = db_sess.query(Note).filter(Note.user_id == current_user.id).order_by(Note.updated_at.desc()).all()
    return render_template("notes_list.html", notes=notes)


@notes_bp.route("/note/create", methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "POST":
        db_sess = create_session()
        note = Note()
        note.title = request.form.get("title")
        note.content = request.form.get("content")
        note.user_id = current_user.id
        note.updated_at = datetime.now()
        db_sess.add(note)
        db_sess.commit()
        flash("Заметка создана", "success")
        return redirect(url_for("notes.notes_list"))
    return render_template("note_form.html", note=None)


@notes_bp.route("/note/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(id):
    db_sess = create_session()
    note = db_sess.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        flash("Заметка не найдена", "danger")
        return redirect(url_for("notes.notes_list"))

    if request.method == "POST":
        note.title = request.form.get("title")
        note.content = request.form.get("content")
        note.updated_at = datetime.now()
        db_sess.commit()
        flash("Заметка обновлена", "success")
        return redirect(url_for("notes.notes_list"))
    return render_template("note_form.html", note=note)


@notes_bp.route("/note/<int:id>/delete", methods=["POST"])
@login_required
def delete_note(id):
    db_sess = create_session()
    note = db_sess.query(Note).filter(Note.id == id, Note.user_id == current_user.id).first()
    if not note:
        flash("Заметка не найдена", "danger")
        return redirect(url_for("notes.notes_list"))

    for attachment in note.attachments:
        path = os.path.join("uploads", attachment.stored_name)
        if os.path.exists(path):
            os.remove(path)
    db_sess.delete(note)
    db_sess.commit()
    flash("Заметка удалена", "success")
    return redirect(url_for("notes.notes_list"))