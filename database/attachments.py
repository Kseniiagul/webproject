import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Attachment(SqlAlchemyBase):
    __tablename__ = "attachments"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    filename = sqlalchemy.Column(sqlalchemy.String)
    stored_name = sqlalchemy.Column(sqlalchemy.String)  # уникальное имя на диске
    file_type = sqlalchemy.Column(sqlalchemy.String)

    note_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("notes.id"))
    note = orm.relationship('Note')
