from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from webapp.model import db, Users, Discussion, Profile, Event, Topic_event, Photo_event
import paginate
import psycopg2
from werkzeug.utils import secure_filename
import os


blueprint = Blueprint('events', __name__)
con = psycopg2.connect(database="engraver", user="postgres", password="111111", host="127.0.0.1", port="5432")
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif'])



@blueprint.route('/all-events')
def all_events():
    events = Event.query.all()
    cur = con.cursor()
    answer = cur.execute(f"Select count(event_type) from Event where event_type = 'Событие'")
    results_event = cur.fetchall()
    print(f"------------------------------------------------------{results_event[0][0]}")
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
    answer = cur.execute(f"Select id from Event where id = {id}")
    results = cur.fetchall()
    number_event = results[0][0]
    if current_user.is_authenticated:
        check_participant = cur.execute(f"Select author_photo from Photo_event where author_photo = '{current_user.login}' and photo_event_id = {id} ")
    results_check_participant = cur.fetchall()
    if results_check_participant == []:
        results_check_participant = None
    else:
        results_check_participant = results_check_participant[0][0]
    print(f"Пользоатель ================================ {results_check_participant}")
    all_photo_event = Photo_event.query
    all_photo_event = all_photo_event.filter(Photo_event.photo_event_id == id)
    all_photo_event = all_photo_event.paginate( page = page, per_page = 12)
    topic_info = Topic_event.query.filter(Topic_event.event_id == id).all()
    topic_event_name = cur.execute(f"Select event_name from event where id = {id}")
    topic_event_name = cur.fetchall()
    topic_event_name = topic_event_name[0][0]
    print(f'===================================={topic_event_name}')
    cur.close()
    return render_template('events/topic_event.html', topic_info = topic_info, topic_event_name = topic_event_name, number_event = str(number_event), all_photo_event = all_photo_event, results_check_participant = results_check_participant)


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



