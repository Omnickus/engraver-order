from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from webapp.model import db, Users, Discussion, Profile, Event, Topic_event, Photo_event, Photo_event_like
import paginate
import psycopg2
from werkzeug.utils import secure_filename
import os
from datetime import datetime


blueprint = Blueprint('events', __name__)
con = psycopg2.connect(database="engraver", user="postgres", password="111111", host="127.0.0.1", port="5432")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif'])



@blueprint.route('/all-events')
def all_events():
    events = Event.query.all()
    return render_template('events/event.html', events = events)


@blueprint.route('/add-event', methods = ['POST'])  
def add_event():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_type = request.form['event_type']
        event_prev_text_first = request.form['event_prev_text_first']
        event_prev_text_second = request.form['event_prev_text_second']
        event_author_login = request.form['event_author_login']
        event_text = request.form['event_text']
        new_event = Event(event_name = event_name, event_type = event_type, event_prev_text_first = event_prev_text_first, event_prev_text_second = event_prev_text_second, event_author_login = event_author_login, event_text = event_text )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('events.all_events'))


@blueprint.route('/delete-event')
def delete_event():
    try:
        delete_event_id = request.args.get('delete_event_id')
        print(delete_event_id)
        cur = con.cursor()
        answer = cur.execute(f"Delete from Event where id  = '{delete_event_id}'")
        con.commit()
        return redirect(url_for('events.all_events'))
    except:
        flash('Извините, что то пошло не так. Сообщите нам об этом')
        return redirect(url_for('events.all_events'))


@blueprint.route('/topic-event/<id>')
def topic_event(id):
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    cur = con.cursor()
    if current_user.is_authenticated:
        try:
            check_participant = cur.execute(f"Select author_photo from Photo_event where author_photo = '{current_user.login}' and photo_event_id = {id} ")
            check_participant = cur.fetchall()
            check_participant = check_participant[0][0]
            print(f"=============={check_participant}")
        except:
            check_participant = None

    print(f"==============2{check_participant}")
    all_photo_event = Photo_event.query
    all_photo_event = all_photo_event.filter(Photo_event.photo_event_id == id)
    all_photo_event = all_photo_event.paginate( page = page, per_page = 12)
    topic_info = Topic_event.query.filter(Topic_event.event_id == id).all()
    topic_event_name = cur.execute(f"Select event_name from event where id = {id}")
    topic_event_name = cur.fetchall()
    topic_event_name = topic_event_name[0][0]
    print(f'===================================={topic_event_name}')
    cur.close()
    return render_template('events/topic_event.html', topic_info = topic_info, topic_event_name = topic_event_name, number_event = id, all_photo_event = all_photo_event, results_check_participant = check_participant, event_id = id)


@blueprint.route('/registr-on-event', methods =['POST'])
def registr_on_event():
    if request.method == 'POST':
        topic_event_name = request.form['topic_event_name']
        event_id = request.form['event_id']
        add_new_participant = Photo_event(first_photo = '',second_photo = '',three_photo = '', author_photo = current_user.login, topic_event_id_photo = event_id, photo_event_id = event_id)
        db.session.add(add_new_participant)
        db.session.commit()

        flash(f"Вы зарегистрировались на участие в {topic_event_name}")
        return redirect(url_for('events.topic_event', id = event_id))


@blueprint.route('/add-discription-to-topic-event', methods = ['POST'])
def add_discription_to_topic_event():
    if request.method == 'POST':
        topic_event_name = request.form['topic_event_name']
        event_id = request.form['event_id']
        topic_event_author = request.form['topic_event_author']
        topic_event_limitations = request.form['topic_event_limitations']
        topic_event_rule_one = request.form['topic_event_rule_one']
        topic_event_rule_two = request.form['topic_event_rule_two']
        topic_event_rule_three = request.form['topic_event_rule_three']
        topic_event_rule_four = request.form['topic_event_rule_four']
        topic_event_rule_five = request.form['topic_event_rule_five']
        topic_event_rule_six = request.form['topic_event_rule_six']
        topic_event_rule_seven = request.form['topic_event_rule_seven']
        topic_event_prerequisites = request.form['topic_event_prerequisites']
        topic_event_prerequisites = request.form['topic_event_prerequisites']
        add_new_topic_event = Topic_event(topic_event_name = topic_event_name, topic_event_author = topic_event_author, topic_event_limitations = topic_event_limitations,
                                            topic_event_rule_one = topic_event_rule_one, topic_event_rule_two = topic_event_rule_two, topic_event_rule_three = topic_event_rule_three,
                                            topic_event_rule_four = topic_event_rule_four, topic_event_rule_five = topic_event_rule_five, topic_event_rule_six =topic_event_rule_six,
                                            topic_event_rule_seven = topic_event_rule_seven, event_id = event_id, topic_event_prerequisites = topic_event_prerequisites)
        db.session.add(add_new_topic_event)
        db.session.commit()
        return redirect(url_for('events.topic_event', id = event_id))


@blueprint.route('/add-like-to-photo-event')
def like_get_way():
    if current_user.is_authenticated:
        way = int(request.args.get('way'))
        photo_id = request.args.get('photo_id')
        like = request.args.get('like')
        event_id = request.args.get('event_id')
        author_like = current_user.login
        print(f"====way={way}======photo_id={photo_id}========like={like}======event_id={event_id}")
        if way == 2010:
            add_like_event.add_like_to_photo_event(photo_id, like, author_like)
            return redirect(url_for('events.topic_event', id = event_id ))
        else:
            flash(f"Error")
            return redirect(url_for('events.topic_event', id = event_id ))
    else:
        event_id = request.args.get('event_id')
        flash(f"Только авторизованные пользователи могут аставлять лайки")
        return redirect(url_for('events.topic_event', id = event_id ))


class add_like_event():
    def add_like_to_photo_event(photo_id, like, author_like):
        if current_user.is_authenticated:
            if like == 'like_up':
                cur = con.cursor()
                cur.execute(f"Select like_up, like_down from photo_event where id = {photo_id}")
                results = cur.fetchall()
                author_like_exist = Photo_event_like.query.filter_by(like_photo_id = photo_id, author_like = author_like).first()
                print(f"==========id==={photo_id}===ПРОВЕРЯЕМ КОЛИЧЕСТВО ЛАЙКОВ В Discussion{results}")
                if results[0][0] == None and results[0][1] == None:
                    print(f"===================ЗАШЕЛ В NONE")
                    cur.execute(f'Update Photo_event set like_up = 1, like_down = 0 where id = {photo_id}')
                    con.commit()
                    add_new_author_like = Photo_event_like(author_like = author_like, like_photo_id = photo_id, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select up, down from Photo_event_like where like_photo_id = {photo_id} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"====================ЭТО АНСВЕР=={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Photo_event set like_up = {results[0][0] + answer[0][1]}, like_down = {results[0][1] - answer[0][1]} where id = {photo_id}')
                        con.commit()
                        cur.execute(f"Update Photo_event_like set up = 1, down = 0 where like_photo_id = {photo_id} and author_like = '{author_like}'")
                        con.commit()
                        cur.close()
                    else:
                        return 'Error'
                else:
                    add_new_author_like = Photo_event_like(author_like = author_like, like_photo_id = photo_id, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Photo_event where id = {photo_id}")
                    results = cur.fetchall()
                    cur.execute(f'Update Photo_event set like_up = {results[0][0] + 1}, like_down = {results[0][1] - 0} where id = {photo_id}')
                    con.commit()
                    
            elif like == 'like_down':
                cur = con.cursor()
                cur.execute(f"Select like_down, like_up from Photo_event where id = {photo_id}")
                results = cur.fetchall()
                author_like_exist = Photo_event_like.query.filter_by(like_photo_id = photo_id, author_like = author_like).first()
                print(f"===================={results}")
                if results[0][0] == None and results[0][1] == None:
                    cur.execute(f'Update Photo_event set like_down = 1, like_up = 0 where id = {photo_id}')
                    con.commit()
                    add_new_author_like = Photo_event_like(author_like = author_like, like_photo_id = photo_id, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select down, up from Photo_event_like where like_photo_id = {photo_id} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"===============like_down====={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Photo_event set like_down = {results[0][0] + answer[0][1]}, like_up = {results[0][1] - answer[0][1]} where id = {photo_id}')
                        con.commit()
                        cur.execute(f"Update Photo_event_like set up = 0, down = 1 where like_photo_id = {photo_id} and author_like = '{author_like}'")
                        cur.close()
                        con.commit()
                else:
                    add_new_author_like = Photo_event_like(author_like = author_like, like_photo_id = photo_id, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Photo_event where id = {photo_id}")
                    results = cur.fetchall()
                    cur.execute(f'Update Photo_event set like_up = {results[0][0] - 0}, like_down = {results[0][1] + 1} where id = {photo_id}')
                    con.commit()
            else:
                return 'Erorr'
        else:
            flash(f'Только авторизованные пользователи могут оставлять голоса')