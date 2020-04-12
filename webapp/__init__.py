import os
from flask import Flask, Blueprint, request, redirect, flash, url_for
import sqlite3
from flask import render_template
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, logout_user
from webapp.model import db, Users, Comment, Profile, Gallary, Discussion, Event, Photo_event
from webapp.forms import LoginForm
from werkzeug.utils import secure_filename
from sqlalchemy.orm import relationship
#Для работы с изображениями
from PIL import Image
#Работа со временем
from datetime import datetime
#Для работы с файлами
import shutil
#PostgreSql
import psycopg2
#import postgresql.driver as pg_driver
from werkzeug.security import generate_password_hash, check_password_hash


from webapp.users_all_profile.views import blueprint as all_pofile_blueprint
from webapp.profile_engraver.views import blueprint as my_profile_engraver
from webapp.discussions.views import blueprint as discussions
from webapp.events.views import blueprint as events



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    
    app.register_blueprint(all_pofile_blueprint)
    app.register_blueprint(my_profile_engraver)
    app.register_blueprint(discussions)
    app.register_blueprint(events)


    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif', 'webp'])
    con = app.config['CONNECT_DB']

    
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(user_id)

    @app.route('/')
    def index():
        return render_template('index/main_page.html')

    @app.route('/profile_engraver/<login>')
    def profile_engraver(login):
        page = request.args.get('page')
        if current_user.is_anonymous or current_user.login != login:
            if page and page.isdigit():
                page = int(page)
            else:
                page = 1
            user_name = login
            user = Users.query.filter_by(login = login).all()
            comments = Comment.query.filter(Comment.user_reciver == login).order_by(Comment.created.desc()).limit(40).all()
            dop_info = Profile.query.filter_by(login = login).all()
            user_gallary = Gallary.query.filter_by(user_author_login = user_name)
            gallary = user_gallary.paginate( page = page, per_page = 6)
            return render_template('users/profile_engraver.html', info = user, user_name = user_name, comments = comments, gallary = gallary, page = page, dop_info = dop_info)

        if page and page.isdigit():
            page = int(page)
        else:
            page = 1
        user_name = login
        user = Users.query.filter_by(login = login).all()
        comments = Comment.query.filter(Comment.user_reciver == login).order_by(Comment.created.desc()).limit(40).all()
        user_gallary = Gallary.query.filter_by(user_author_login = login)
        dop_info = Profile.query.filter_by(login = login).all()
        print(f"{dop_info}===========================================================================================")
        gallary = user_gallary.paginate( page = page, per_page = 6)
        return render_template('users/profile_engraver.html', info = user, user_name = user_name, comments = comments, gallary = gallary, page = page, dop_info = dop_info)


    @app.route('/add-info-into-profile', methods = ['POST'])
    def add_info_into_prifile():
        if request.method == 'POST':
            city = request.form['city']
            region = request.form['region']
            brifdate = request.form['brifdate']
            work_profile = request.form['work_profile']
            experience = request.form['experience']
            link_you_tube = request.form['link_you_tube']
            link_you_instagram = request.form['link_you_instagram']
            about_himsefl_profile = request.form['about_himsefl_profile']
            link_you_vkontakte = request.form['link_you_vkontakte']
            info_profile_login = current_user.login
            owner_id = current_user.id
            info_exist = Profile.query.filter_by(login = current_user.login).first()
            if not info_exist:
                info_exist = Profile(owner_id = current_user.id, info_profile_login = current_user.login)
                db.session.add(info_exist)
                db.session.commit()
            
            if city == '' and info_exist.city == None:
                info_exist.city = None
                db.session.commit()
            elif city == '' and info_exist.city != None:
                city = info_exist.city
            else:
                info_exist.city = city
                #db.session.commit()
            if region == '' and info_exist.region == None:
                info_exist.region = None
                db.session.commit()
            elif region == '' and info_exist.region != None:
                region = info_exist.region
            else:
                info_exist.region = region
                #db.session.commit()
            if brifdate == '' and info_exist.brifdate == None:
                info_exist.brifdate = None
                db.session.commit()
            elif brifdate == '' and info_exist.brifdate != None:
                brifdate = info_exist.brifdate
            else:
                info_exist.brifdate = brifdate
                #db.session.commit()
            if work_profile == '' and info_exist.work_profile == None:
                info_exist.work_profile = None
                db.session.commit()
            elif work_profile == '' and info_exist.work_profile != None:
                work_profile = info_exist.work_profile
            else:
                info_exist.work_profile = work_profile
                #db.session.commit()
            if experience == '' and info_exist.experience == None:
                info_exist.experience = None
                db.session.commit()
            elif experience == '' and info_exist.experience != None:
                experience = info_exist.experience
            else:
                info_exist.experience = experience
                #db.session.commit()
            if link_you_tube == '' and info_exist.link_you_tube == None:
                info_exist.link_you_tube = None
                db.session.commit()
            elif link_you_tube == '' and info_exist.link_you_tube != None:
                link_you_tube = info_exist.link_you_tube
            else:
                info_exist.link_you_tube = link_you_tube
                #db.session.commit()
            if link_you_instagram == '' and info_exist.link_you_instagram == None:
                info_exist.link_you_instagram == None
                db.session.commit()
            elif link_you_instagram == '' and info_exist.link_you_instagram != None:
                link_you_instagram = info_exist.link_you_instagram
            else:
                info_exist.link_you_instagram = link_you_instagram
                #db.session.commit()
            if link_you_vkontakte == '' and info_exist.link_you_vkontakte == None:
                info_exist.link_you_vkontakte == None
                db.session.commit()
            elif link_you_vkontakte == '' and info_exist.link_you_vkontakte != None:
                info_exist.link_you_vkontakte = link_you_vkontakte
            else:
                info_exist.link_you_vkontakte = link_you_vkontakte
                #db.session.commit()
            if about_himsefl_profile =='' and info_exist.about_himsefl_profile == None:
                info_exist.about_himsefl_profile == None
                db.session.commit()
            elif about_himsefl_profile == '' and info_exist.about_himsefl_profile != None:
                about_himsefl_profile = info_exist.about_himsefl_profile
            else:
                info_exist.about_himsefl_profile = about_himsefl_profile
                #db.session.commit()
                
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        else:
            return 'Hello'

    @app.route('/delete-info-into-profile', methods = ['GET'])
    def delete_info_into_profile():
        info_delete = request.args.get('info_delete')
        if info_delete == 'city':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.city = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'region':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.region = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'brifdate':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.brifdate = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'work_profile':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.work_profile = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'experience':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.experience = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'link_you_tube':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.link_you_tube = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'link_you_instagram':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.link_you_instagram = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'link_you_vkontakte':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.link_you_vkontakte = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        elif info_delete == 'about_himsefl_profile':
            info_exist = Profile.query.filter_by(owner_id = current_user.id).first()
            info_exist.about_himsefl_profile = None
            db.session.commit()
            return redirect(url_for('profile_engraver', login = current_user.login))
        else:
            flash('Произошла ошибка. Пожалуйста, сообщите нам об этом. Связаться с нами вы можете в подвале сайта')
            return redirect(url_for('profile_engraver', login = current_user.login))


    class Photo_editor():
        def photo_editor_event(file, topic_event_id, author_photo, filename):
            print(f"===================ЗАШЕЛ В КЛАСС======================")
            #file.save(os.path.join(app.config['ADD_PHOTO_TO_EVENT'] + '\\' + topic_event_id + '\\' + author_photo + '\\', filename))
            im = Image.open(file) # Открываем файл для работы
            width = im.size[0]  # Определяем ширину
            height = im.size[1]  # Определяем высоту
            if width > height or width == height:
                x = width - height
                x2 = x // 2
                im2 = im.crop((x2, 0, width - x2, height))
            elif height > width:
                x = height - width
                x2 = x // 2
                im2 = im.crop((0, x2, width, height - x2))

            im2.thumbnail((800, 800)) # Уменьшаем масштаб
            im2.save(os.path.join(app.config['ADD_PHOTO_TO_EVENT'] + '\\' + topic_event_id + '\\' + author_photo + '\\' + filename))
            return im2

        def photo_editor_avatar(file, filename):
            im = Image.open(file)
            width = im.size[0]  # Определяем ширину
            height = im.size[1]  # Определяем высоту
            if width > height:
                x = width - height
                x2 = x // 2
                im2 = im.crop((x2, 0, width - x2, height))
            elif height > width:
                x = height - width
                x2 = x // 2
                im2 = im.crop((0, x2, width, height - x2))
            im2.thumbnail((400, 400))
            im2.save(app.config['UPLOAD_AVATAR'] + '\\' f'{current_user.login}\\{filename}')
            return True

        def photo_editor_gallary(file, filename):
            im = Image.open(file)
            width = im.size[0]  # Определяем ширину
            height = im.size[1]  # Определяем высоту
            if width > height:
                x = width - height
                x2 = x // 2
                im2 = im.crop((x2, 0, width - x2, height))
            elif height > width:
                x = height - width
                x2 = x // 2
                im2 = im.crop((0, x2, width, height - x2))
            print(f"Success")
            im2.thumbnail((400, 400))
            im2.save(os.path.join(app.config['UPLOAD_PHOTO_IN_GALLARY'] + '\\' + current_user.login + '\\gallary' + '\\' + filename))
            return im2


    @app.route('/login')
    def login():
        print(current_user)
        login_form = LoginForm()
        return render_template('users/user_login.html', form = login_form)

    @app.route('/registartion')
    def registration():
        if current_user.is_authenticated:
            flash('Вы уже зарегистрированы')
        return render_template('users/user_registration.html')

    @app.route('/process-login', methods = ['POST'])
    def process_login():
        form = LoginForm()
        if current_user.is_authenticated:
            flash('Вы уже авторизованы')
            return redirect(url_for('index'))
        elif form.validate_on_submit():
            user = Users.query.filter(Users.login == form.login.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы авторизовались')
                return redirect(url_for('profile_engraver', login = current_user.login))
        flash('Неправильный логин или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        if current_user.is_anonymous:
            flash('Вы не авторизованы')
            return redirect(url_for('index'))
        else:
            logout_user()
            flash('Вы вышли')
            return redirect(url_for('index'))



    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 

    @app.route('/delete_avatar', methods = ['POST'])
    def delete_avatar():
        if request.method =='POST':
            try:
                filename = Users.query.filter_by( login = current_user.login).first()
                path = os.path.join(app.config['UPLOAD_AVATAR'] + '\\' + current_user.login, filename.images )
                os.remove(path)
                return redirect(url_for('profile_engraver', login = current_user.login))
            except FileNotFoundError:
                flash('Аватар удален')
                return redirect(url_for('profile_engraver', login = current_user.login))
        return redirect(url_for('index'))
    
    @app.route('/process_registartion', methods = ['POST'])
    def process_registration():
        if current_user.is_authenticated:
            flash('Вы авторизованы, у вас есть учетная запись')
            return redirect(url_for('index'))
        with app.app_context():
            first_name = request.form['first_name']
            second_name = request.form['second_name']
            login = request.form['login']
            password1 = request.form['password1']
            password2 = request.form['password2']
            email = request.form['email']
            image = 'avatar_none.png'

            if len(first_name) < 2:
                flash("Строка имени не заполнена")
                return redirect(url_for('registration'))

            if ' ' in first_name:
                flash('В имени не может быть пробелов')
                return redirect(url_for('registration'))

            if len(second_name) < 2:
                flash("Строка фамилии не заполнена")
                return redirect(url_for('registration'))

            if ' ' in second_name:
                flash('В фамилии не может быть пробелов')
                return redirect(url_for('registration'))

            if len(login) <= 3 or len(login) > 15:
                flash("Логин должен содержать от 3-х до 15-ти символов и не может содержать пробелов")
                return redirect(url_for('registration'))
            
            if ' ' in login:
                flash('В логине не может быть пробелов')
                return redirect(url_for('registration'))

            if ' ' in password1:
                flash('В пароле не может быть пробелов')
                return redirect(url_for('registration'))

            if Users.query.filter(Users.login ==  login).count():
                flash('Пользователь с таким именем существует')
                return redirect(url_for('registration'))
            
            if Users.query.filter(Users.email ==  email).count():
                flash('Пользователь с таким email существует')
                return redirect(url_for('registration'))

            if not password1 == password2:
                flash('Пароли не одинаковые')
                return redirect(url_for('registration'))
            
            try:
                new_user = Users(role = 'user', status = 'active', first_name = first_name, second_name = second_name, login = login, email = email, images = image)
                new_user.set_password(password1)
                db.session.add(new_user)
                db.session.commit()
            except:
                flash(f"Произошла ошибка записи в таблицу User")
                return redirect(url_for('registration'))
            try:
                cur = con.cursor()
                answer = cur.execute(f"Select id from users where login = '{login}'")
                results = cur.fetchall()
                create_profile_for_user = Profile(first_name = first_name, second_name = second_name, login = login, info_profile_login = login, owner_id = results[0][0] )
                db.session.add(create_profile_for_user)
                db.session.commit()
            except:
                flash(f"Произошла ошибка записи в таблицу Profile")
                return redirect(url_for('registration'))  
            
            user = Users.query.filter(Users.login == login).first()
            if user and user.check_password(password1):
                login_user(user)
            try:
                os.mkdir(app.config['UPLOAD_AVATAR'] + '\\' + current_user.login)
                shutil.copy(app.config['UPLOAD_AVATAR'] + '\\' + 'avatar_none' + '\\' + 'avatar_none.png' ,app.config['UPLOAD_AVATAR'] + '\\' + current_user.login + '\\' + 'avatar_none.png') 
            except FileExistsError:
                return redirect(url_for('profile_engraver', login = login))

            return redirect(url_for('profile_engraver' , login = login))


    @app.route('/add_comment', methods = ['POST'])
    def add_comment():
        if request.method == 'POST' and current_user.is_authenticated:
            text_comment = request.form['text']
            print(text_comment)
            if len(text_comment) <= 2:
                recipient_engraver = request.form['recipient_engraver']
                return f"Очень маленькое сообщение"

            author_engraver = request.form['author_engraver']
            recipient_engraver = request.form['recipient_engraver']
            login = Users.query.filter_by(login = recipient_engraver).first()
            new_comment = Comment(text = text_comment, user_reciver = recipient_engraver, user_author = current_user.id, created = datetime.now())
            db.session.add(new_comment)
            db.session.commit()
            return 'Сообщение отправлено'
        else:
            recipient_engraver = request.form['recipient_engraver']
            flash('Оставлять комментарии могут только авторизованные пользователи')
            return redirect(url_for('profile_engraver', login = recipient_engraver))
        return 'Hello'


    @app.route('/delete-comment/', methods = ['POST', 'GET'])
    def delete_comment():
        try:
            user_name = request.form['comment_user']
            comment_id = request.form['comment_id']
            print(f"{user_name}_____{comment_id}")
            comment_del = Comment.query.filter_by(id = comment_id).first()
            db.session.delete(comment_del)
            db.session.commit()
            return 'Сообщение удалено'
        except:
            return f'Что то пошло не так + {NameError}'


    @app.route('/crop-center')
    def crop_center(pil_img):
        new_crop = (pil_img, min(pil_img.size), min(pil_img.size))
        print(new_crop)
        return new_crop


    @app.route('/upload_file', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            try:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    try:
                        os.mkdir(app.config['UPLOAD_AVATAR'] + '\\' + current_user.login)
                    except FileExistsError:
                        pass

                    try:
                        old_avatar = Users.query.filter_by( login = current_user.login).first()
                        path = os.path.join(app.config['UPLOAD_AVATAR'] + '\\' + current_user.login, old_avatar.images )
                        os.remove(path)
                    except:
                        pass

                    try:
                        Photo_editor.photo_editor_avatar(file, filename)
                        avatar_engraver = Users.query.filter_by( login = current_user.login).first()
                        avatar_engraver.images = filename
                        db.session.commit()
                        flash('Фаил загружен')
                    except:
                        flash(f"Что-то пошло не так. Попробуйте снова")
                    return redirect(url_for('profile_engraver', login = current_user.login))

                user_name = current_user.login
                flash('Вы не выбрали фаил или загружаемый фаил не подходит. Выберите "PNG", "JPG" или "JPEG"')
                return redirect(url_for('profile_engraver', login = current_user.login))
            except TypeError:
                flash('Вы не выбрали фаил')
                return redirect(url_for('profile_engraver', login = current_user.login))
        else:
            flash('Неверный метот передачи файла')
            return redirect(url_for('profile_engraver', login = current_user.login))
    

    @app.route('/add-photo-in-gallary', methods = ['POST'])
    def add_photo_in_gallary():
        if request.method == 'POST':
            try:
                file = request.files['file']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    photo_exist = Gallary.query.filter_by(name_photo = filename).first()
                    cur = con.cursor()
                    answer = cur.execute(f"Select name_photo from gallary where user_author_login = '{current_user.login}'")
                    results = cur.fetchall()
                    if results == []:
                        try:
                            os.mkdir(app.config['UPLOAD_PHOTO_IN_GALLARY'] + '\\' + current_user.login + '\\' + 'gallary' )
                        except:
                            pass
                        try:
                            Photo_editor.photo_editor_gallary(file, filename)
                            save_photo = Gallary(name_photo = filename, user_author = current_user.id, user_author_login = current_user.login)
                            db.session.add(save_photo)
                            db.session.commit()
                            flash('Фаил загружен')
                            return redirect(url_for('profile_engraver', login = current_user.login))
                        except:
                            flash('Произошла ошибка. Попробуйте снова. 010')
                            return redirect(url_for('profile_engraver', login = current_user.login))
                    else:
                        for i in results:
                            if i[0] == filename:
                                flash('У вас уже загружена такая фотография')
                                return redirect(url_for('profile_engraver', login = current_user.login))
                            else:
                                try:
                                    os.mkdir(app.config['UPLOAD_PHOTO_IN_GALLARY'] + '\\' + current_user.login + '\\' + 'gallary' )
                                except:
                                    pass
                                try:
                                    Photo_editor.photo_editor_gallary(file, filename)
                                    save_photo = Gallary(name_photo = filename, user_author = current_user.id, user_author_login = current_user.login)
                                    db.session.add(save_photo)
                                    db.session.commit()
                                    flash('Фаил загружен')
                                    return redirect(url_for('profile_engraver', login = current_user.login))
                                except:
                                    flash('Произошла ошибка. Попробуйте снова.')
                                    return redirect(url_for('profile_engraver', login = current_user.login))

                user_name = current_user.login
                flash('Вы не выбрали фаил или загружаемый фаил не подходит. Выберите "PNG", "JPG" или "JPEG"')
                return redirect(url_for('profile_engraver', login = user_name))
            except TypeError:
                flash('Вы не выбрали фаил')
                return redirect(url_for('profile_engraver', login = current_user.login))
        else:
            flash('Неверный метот передачи файла')
            return redirect(url_for('profile_engraver', login = current_user.login))

    @app.route('/del-photo', methods = ['POST'])
    def photo_del():
        if request.method == 'POST':
            try:
                name_photo = request.form['del']
                photo_del = Gallary.query.filter(Gallary.name_photo == name_photo, Gallary.user_author_login == current_user.login).first()
                db.session.delete(photo_del)
                db.session.commit()
                path = os.path.join(app.config['UPLOAD_PHOTO_IN_GALLARY'] + '\\' + current_user.login + '\\galarry' + '\\' + name_photo )
                os.remove(path)
            finally:
                return redirect(url_for('profile_engraver', login = current_user.login))
        return "Hello"


    @app.route('/add-photo-to-event', methods = ['POST'])
    def add_photo_to_event():
        if request.method == 'POST':
            file = request.files['file']
            topic_event_id = request.form['topic_event_id']
            author_photo = request.form['author_photo']
            number_photo = request.form['number_photo']
            topic_event_name = request.form['topic_event_name']
            topic_event_name = topic_event_name.strip()
            topic_event_id = topic_event_id.strip()
            cur = con.cursor()
            answer = cur.execute(f"Select {number_photo} from Photo_event where author_photo = '{author_photo}' and photo_event_id = '{topic_event_id}'")
            photo_exist = cur.fetchall()
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    os.mkdir(app.config['ADD_PHOTO_TO_EVENT'] + '\\' + topic_event_id )
                except FileExistsError:
                    pass
                try:
                    os.mkdir(app.config['ADD_PHOTO_TO_EVENT'] + '\\' + topic_event_id + '\\' + author_photo)
                except FileExistsError:
                    pass
                try:
                    os.remove(os.path.join(app.config['ADD_PHOTO_TO_EVENT'] + '\\' + topic_event_id + '\\' + author_photo + '\\', photo_exist[0][0]))
                except:
                    pass
                try:
                    Photo_editor.photo_editor_event(file, topic_event_id, author_photo, filename)
                except:
                    flash(f"Произошла ошибка. Попробуйте повторить загрузку. При повторной ошибке, пожалуйста, сообщите нам об этом")

                cur = con.cursor()
                answer = cur.execute(f"Select first_photo, second_photo, three_photo, author_photo from Photo_event where author_photo = '{author_photo}' and photo_event_id = '{topic_event_id}'")
                results = cur.fetchall()
                if results != []:
                    if number_photo == 'first_photo':
                        try:
                            cur = con.cursor()
                            cur.execute(f"Update Photo_event set first_photo = '{filename}' where author_photo = '{author_photo}' and photo_event_id = '{topic_event_id}'")
                            cur.close()
                            con.commit()
                            return redirect(url_for('events.topic_event',id = topic_event_id ))
                        except:
                            flash(f"Произошла ошибка при загрузке первой фотографии {filename}")
                            return redirect(url_for('events.topic_event',id = topic_event_id ))
                    elif number_photo == 'second_photo':
                        try:
                            cur = con.cursor()
                            cur.execute(f"Update Photo_event set second_photo = '{filename}' where author_photo = '{author_photo}' and photo_event_id = '{topic_event_id}'")
                            cur.close()
                            con.commit()
                            return redirect(url_for('events.topic_event',id = topic_event_id ))
                        except:
                            flash(f"Произошла ошибка при загрузке второй фотографии {filename}")
                            return redirect(url_for('events.topic_event',id = topic_event_id ))
                    else:
                        try:
                            cur = con.cursor()
                            cur.execute(f"Update Photo_event set three_photo = '{filename}' where author_photo = '{author_photo}' and photo_event_id = '{topic_event_id}'")
                            cur.close()
                            con.commit()
                            return redirect(url_for('events.topic_event',id = topic_event_id ))
                        except:
                            flash(f"Произошла ошибка при загрузке третьей фотографии {filename}")
                            return redirect(url_for('events.topic_event',id = topic_event_id ))
                else:
                    add_new_photo = Photo_event(first_photo = filename, second_photo = '' , three_photo = '', author_photo = author_photo, topic_event_id_photo = topic_event_id, event_id = topic_event_id)
                    db.session.add(add_new_photo)
                    db.session.commit()
                    return redirect(url_for('events.topic_event',id = topic_event_id ))

                flash(f'Что то пошло не так')
                return redirect(url_for('events.topic_event',id = topic_event_id ))

            flash(f'Метод передачи файла не подходит')
            return redirect(url_for('events.topic_event',id = topic_event_id ))
        flash(f'Метод передачи файла не подходит')
        return redirect(url_for('events.topic_event',id = topic_event_id ))
    return app
