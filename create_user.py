from getpass import getpass
import sys
from webapp import create_app
from webapp.model import db, Users

app = create_app()

with app.app_context():
    name = input('Введите имя')
    second_name = input('Введите фамилию')
    email = input('Введите вашу почту')
    login = input('Введите логин')

    if Users.query.filter(Users.login == login).count():
        print('Прльзователь с таким именем уже есть')
        sys.exit(0)

    password1 = getpass('Введиете пароль')
    password2 = getpass('Повторите пароль')

    if not password1 == password2:
        print('Пароли не одинаковые')
        sys.exit()

    new_user = Users(first_name = name, second_name = second_name, login = login, email = email, image = 'avatar_none.png')
    new_user.set_password(password1)
    db.session.add(new_user)
    db.session.commit()
    print('Вы зарегистрировались')