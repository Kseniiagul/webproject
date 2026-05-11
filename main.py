from datetime import datetime
from forms.user import RegisterForm
from database.users import User
from database import db_session
from flask import render_template, redirect, Flask

from routes.export import export_note
from routes.view import view_note
from routes.api import api_note

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш-секретный-ключ-здесь'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            created_at=datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/notes.db")

    app.register_blueprint(export_note)
    app.register_blueprint(view_note)
    app.register_blueprint(api_note)

    app.run()


if __name__ == '__main__':
    main()
