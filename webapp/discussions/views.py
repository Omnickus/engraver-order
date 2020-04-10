from flask import Blueprint, render_template, redirect, request, url_for, flash
from webapp.model import db, Users, Comment, Profile, Gallary, Discussion, Discuss_comments, Discussion_like, Comment_discuss_comments, Discuss_comments_like, Comment_discuss_comments_like
from flask_login import LoginManager, login_user, current_user, logout_user
from datetime import datetime
import sqlite3
import psycopg2
blueprint = Blueprint('discussions', __name__)
con = psycopg2.connect(database="engraver", user="postgres", password="111111", host="127.0.0.1", port="5432")


@blueprint.route('/discussion/')
def discussion():
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    discuss = Discussion.query
    all_discuss = discuss.order_by(Discussion.created_discuss).paginate( page = page, per_page = 20)
    return render_template('index/discussions.html', all_discuss = all_discuss, page =page)


@blueprint.route('/add-discussion', methods = ['POST'])
def add_discuss():
    if request.method == 'POST':
        name_discuss = request.form['name_discuss']
        exist_discuss = Discussion.query.filter_by(name_discuss = name_discuss).first()
        if exist_discuss:
            flash('Такое обсуждение уже есть')
            return redirect(url_for('discussions.discussion'))
        else:
            author_discuss = request.form['author_discuss']
            author_discuss_login = request.form['author_discuss_login']
            new_discuss = Discussion(name_discuss = name_discuss, author_discuss = author_discuss, author_discuss_login = author_discuss_login, created_discuss = datetime.now())
            db.session.add(new_discuss)
            db.session.commit()
            flash
            return redirect(url_for('discussions.discussion'))
    else:
        flash('Что то пошло не так :(')
        return redirect(url_for('discussions.discussion'))

@blueprint.route('/delete-discussion', methods = ['GET'])
def delete_discussion():
    name_discuss = request.args.get('name_discuss')
    if request.method == 'GET':
        try:
            discuss_exist = Discussion.query.filter_by(name_discuss = name_discuss).first()
            db.session.delete(discuss_exist)
            db.session.commit()
            return redirect(url_for('discussions.discussion'))
        except:
            flash('Что то пошло не так. Пожалуйста сообщите нам об этом.')
            return redirect(url_for('discussions.discussion'))

@blueprint.route('/add-like-to-discussion')
def add_like_to_discussion():
    if current_user.is_authenticated:
        way = int(request.args.get('way'))
        discuss_id = request.args.get('id')
        topic_id = request.args.get('topic_id')
        author_like = current_user.login
        if way == 1010:
            like = request.args.get('like')
            #name_discuss = request.args.get('name_discuss')
            Like_in_discussion.add_like_to_discussion_all_discuss(discuss_id, like, author_like)
            return redirect(url_for('discussions.discussion'))
        elif way == 1020:
            comment_id = request.args.get('id')
            like = request.args.get('like')
            Like_in_discussion.add_like_to_comment_in_topic_discuss(comment_id, like, author_like)
            return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = topic_id))
        elif way == 1030:
            like = request.args.get('like')
            comment_id_second = request.args.get('id')
            Like_in_discussion.add_like_to_comment_in_topic_discuss_comment(comment_id_second, like, author_like)
            return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = topic_id))
        else:
            flash(f"Ошибка")
            return redirect(url_for('discussions.discussion'))
    else:
        flash(f"Только авторизованные пользователи могут голосовать")
        return redirect(url_for('discussions.discussion'))


@blueprint.route('/topic-of-discussion/<id_topic_discuss>/')
def topic_of_discussion(id_topic_discuss):
    id_topic_discuss = id_topic_discuss
    topic_discuss = Discussion.query.filter_by(id = id_topic_discuss).first()
    comment_discussion = Discuss_comments.query.filter_by(discuss_id = id_topic_discuss).order_by(Discuss_comments.discuss_comment_created).all()
    cur = con.cursor()
    cur.execute(f"Select cdc.id, cdc.discuss_comment_id ,cdc.text, cdc.date_created, cdc.user_login, cdc.like_up, cdc.like_down from Comment_discuss_comments cdc inner join Discuss_comments dc on cdc.discuss_comment_id = dc.id order by cdc.date_created asc")
    comment_in_comments = cur.fetchall()
    cur.close()
    return render_template('index/topic_of_discussion.html', comment_discussion = comment_discussion, topic_discuss = topic_discuss, comment_in_comments = comment_in_comments )


@blueprint.route('/add-comment-to-discussion', methods = ['POST'])
def add_comment_to_discussion():
    if request.method == 'POST':
        comment_text = request.form['text']
        discuss_id = request.form['id_discuss']
        author_comment = request.form['author_comment']
        add_discuss_comment = Discuss_comments(text = comment_text, discuss_comment_created = datetime.now(), user_login = author_comment, discuss_id = discuss_id )
        db.session.add(add_discuss_comment)
        db.session.commit()
        return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = discuss_id))
    else:
        flash(f"Error")
        return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = discuss_id))


@blueprint.route('/delete-comment-of-discussion', methods = ['GET'])
def delete_comment_of_discussion():
    id_comment = request.args.get('id_comment')
    discuss_id = request.args.get('discuss_id')
    try:
        comment_del_topic_discuss = Discuss_comments.query.filter_by(id = id_comment).first()
        db.session.delete(comment_del_topic_discuss)
        db.session.commit()
        return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = discuss_id))
    except:
        flash('Непредвиденная ошибка. По возможности, сообщите нам об этом через форму обратной связи в подвале сайта')
        return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = discuss_id))


@blueprint.route('/add-comment-to-comment', methods = ['POST'])
def add_comment_to_comment():
    if request.method == 'POST':
        comment_text = request.form['comment_text_to_comment']
        to_comment = request.form['comment_id']
        id_discuss = request.form['id_discuss']
        try:
            add_comment = Comment_discuss_comments(text = comment_text, user_login = current_user.login, date_created = datetime.now(), discuss_comment_id = to_comment)
            db.session.add(add_comment)
            db.session.commit()
            return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = id_discuss))
        except:
            flash(f"Что то пошло не так с добавлением комментария")
            return redirect(url_for('discussions.topic_of_discussion', id_topic_discuss = id_discuss))
    else:
        return "Hello"


class Like_in_discussion():
    def add_like_to_discussion_all_discuss(discuss_id, like, author_like):
        if current_user.is_authenticated:
            if like == 'like_up':
                cur = con.cursor()
                cur.execute(f"Select like_up, like_down from Discussion where id = {discuss_id}")
                results = cur.fetchall()
                author_like_exist = Discussion_like.query.filter_by(discuss_id = discuss_id, author_like = author_like).first()
                print(f"==========id==={discuss_id}===ПРОВЕРЯЕМ КОЛИЧЕСТВО ЛАЙКОВ В Discussion{results}")
                if results[0][0] == None and results[0][1] == None:
                    print(f"===================ЗАШЕЛ В NONE")
                    cur.execute(f'Update Discussion set like_up = 1, like_down = 0 where id = {discuss_id}')
                    con.commit()
                    add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select up, down from Discussion_like where discuss_id = {discuss_id} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"====================ЭТО АНСВЕР=={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Discussion set like_up = {results[0][0] + answer[0][1]}, like_down = {results[0][1] - answer[0][1]} where id = {discuss_id}')
                        con.commit()
                        cur.execute(f"Update Discussion_like set up = 1, down = 0 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                        con.commit()
                        cur.close()
                    else:
                        return 'Error'
                else:
                    add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Discussion where id = {discuss_id}")
                    results = cur.fetchall()
                    cur.execute(f'Update Discussion set like_up = {results[0][0] + 1}, like_down = {results[0][1] - 0} where id = {discuss_id}')
                    con.commit()
                    
            elif like == 'like_down':
                cur = con.cursor()
                cur.execute(f"Select like_down, like_up from Discussion where id = {discuss_id}")
                results = cur.fetchall()
                author_like_exist = Discussion_like.query.filter_by(discuss_id = discuss_id, author_like = author_like).first()
                print(f"===================={results}")
                if results[0][0] == None and results[0][1] == None:
                    cur.execute(f'Update Discussion set like_down = 1, like_up = 0 where id = {discuss_id}')
                    con.commit()
                    add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select down, up from Discussion_like where discuss_id = {discuss_id} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"===============like_down====={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Discussion set like_down = {results[0][0] + answer[0][1]}, like_up = {results[0][1] - answer[0][1]} where id = {discuss_id}')
                        con.commit()
                        cur.execute(f"Update Discussion_like set up = 0, down = 1 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                        cur.close()
                        con.commit()
                else:
                    add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Discussion where id = {discuss_id}")
                    results = cur.fetchall()
                    cur.execute(f'Update Discussion set like_up = {results[0][0] - 0}, like_down = {results[0][1] + 1} where id = {discuss_id}')
                    con.commit()
            else:
                return 'Erorr'
        else:
            flash(f'Только авторизованные пользователи могут оставлять голоса')

    
    def add_like_to_comment_in_topic_discuss(comment_id, like, author_like):
        if current_user.is_authenticated:
            if like == 'like_up':
                cur = con.cursor()
                cur.execute(f"Select like_up, like_down from Discuss_comments where id = {comment_id}")
                results = cur.fetchall()
                author_like_exist = Discuss_comments_like.query.filter_by(discuss_comment_id = comment_id, author_like = author_like).first()
                print(f"==========id==={comment_id}===ПРОВЕРЯЕМ КОЛИЧЕСТВО ЛАЙКОВ В Discussion{results}")
                if results[0][0] == None and results[0][1] == None:
                    print(f"===================ЗАШЕЛ В NONE")
                    cur.execute(f'Update Discuss_comments set like_up = 1, like_down = 0 where id = {comment_id}')
                    con.commit()
                    add_new_author_like = Discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select up, down from Discuss_comments_like where discuss_comment_id = {comment_id} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"====================ЭТО АНСВЕР=={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Discuss_comments set like_up = {results[0][0] + answer[0][1]}, like_down = {results[0][1] - answer[0][1]} where id = {comment_id}')
                        con.commit()
                        cur.execute(f"Update Discuss_comments_like set up = 1, down = 0 where discuss_comment_id = {comment_id} and author_like = '{author_like}'")
                        con.commit()
                        cur.close()
                    else:
                        return 'Error'
                else:
                    add_new_author_like = Discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Discuss_comments where id = {comment_id}")
                    results = cur.fetchall()
                    cur.execute(f'Update Discuss_comments set like_up = {results[0][0] + 1}, like_down = {results[0][1] - 0} where id = {comment_id}')
                    con.commit()
                    
            elif like == 'like_down':
                cur = con.cursor()
                cur.execute(f"Select like_down, like_up from Discuss_comments where id = {comment_id}")
                results = cur.fetchall()
                author_like_exist = Discuss_comments_like.query.filter_by(discuss_comment_id = comment_id, author_like = author_like).first()
                print(f"===================={results}")
                if results[0][0] == None and results[0][1] == None:
                    cur.execute(f'Update Discuss_comments set like_down = 1, like_up = 0 where id = {comment_id}')
                    con.commit()
                    add_new_author_like = Discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select down, up from Discuss_comments_like where discuss_comment_id = {comment_id} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"===============like_down====={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Discuss_comments set like_down = {results[0][0] + answer[0][1]}, like_up = {results[0][1] - answer[0][1]} where id = {comment_id}')
                        con.commit()
                        cur.execute(f"Update Discuss_comments_like set up = 0, down = 1 where discuss_comment_id = {comment_id} and author_like = '{author_like}'")
                        cur.close()
                        con.commit()
                else:
                    add_new_author_like = Discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Discuss_comments where id = {comment_id}")
                    results = cur.fetchall()
                    cur.execute(f'Update Discuss_comments set like_up = {results[0][0] - 0}, like_down = {results[0][1] + 1} where id = {comment_id}')
                    con.commit()
            else:
                return 'Erorr'
        else:
            flash(f'Только авторизованные пользователи могут оставлять голоса')


    def add_like_to_comment_in_topic_discuss_comment(comment_id_second, like, author_like):
        if current_user.is_authenticated:
            print(f"=========================={comment_id_second}")
            if like == 'like_up':
                cur = con.cursor()
                cur.execute(f"Select like_up, like_down from Comment_discuss_comments where id = {comment_id_second}")
                results = cur.fetchall()
                author_like_exist = Comment_discuss_comments_like.query.filter_by(discuss_comment_id = comment_id_second, author_like = author_like).first()
                print(f"==========id==={comment_id_second}===ПРОВЕРЯЕМ КОЛИЧЕСТВО ЛАЙКОВ В Discussion{results}")
                if results[0][0] == None and results[0][1] == None:
                    print(f"===================ЗАШЕЛ В NONE")
                    cur.execute(f'Update Comment_discuss_comments set like_up = 1, like_down = 0 where id = {comment_id_second}')
                    con.commit()
                    add_new_author_like = Comment_discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id_second, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select up, down from Comment_discuss_comments_like where discuss_comment_id = {comment_id_second} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"====================ЭТО АНСВЕР=={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Comment_discuss_comments set like_up = {results[0][0] + answer[0][1]}, like_down = {results[0][1] - answer[0][1]} where id = {comment_id_second}')
                        con.commit()
                        cur.execute(f"Update Comment_discuss_comments_like set up = 1, down = 0 where discuss_comment_id = {comment_id_second} and author_like = '{author_like}'")
                        con.commit()
                        cur.close()
                    else:
                        return 'Error'
                else:
                    add_new_author_like = Comment_discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id_second, date_like = datetime.now(), down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Comment_discuss_comments where id = {comment_id_second}")
                    results = cur.fetchall()
                    cur.execute(f'Update Comment_discuss_comments set like_up = {results[0][0] + 1}, like_down = {results[0][1] - 0} where id = {comment_id_second}')
                    con.commit()
                    
            elif like == 'like_down':
                cur = con.cursor()
                cur.execute(f"Select like_down, like_up from Comment_discuss_comments where id = {comment_id_second}")
                results = cur.fetchall()
                author_like_exist = Comment_discuss_comments_like.query.filter_by(discuss_comment_id = comment_id_second, author_like = author_like).first()
                print(f"===================={results}")
                if results[0][0] == None and results[0][1] == None:
                    cur.execute(f'Update Comment_discuss_comments set like_down = 1, like_up = 0 where id = {comment_id_second}')
                    con.commit()
                    add_new_author_like = Comment_discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id_second, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                elif author_like_exist and results[0][0] != None and results[0][1] != None:
                    cur.execute(f"select down, up from Comment_discuss_comments_like where discuss_comment_id = {comment_id_second} and author_like = '{author_like}'")
                    answer = cur.fetchall()
                    print(f"===============like_down====={answer}")
                    if answer[0][0] == 1:
                        flash(f"Вы уже проголосовали за эту запись")
                    elif answer[0][0] == 0:
                        cur.execute(f'Update Comment_discuss_comments set like_down = {results[0][0] + answer[0][1]}, like_up = {results[0][1] - answer[0][1]} where id = {comment_id_second}')
                        con.commit()
                        cur.execute(f"Update Comment_discuss_comments_like set up = 0, down = 1 where discuss_comment_id = {comment_id_second} and author_like = '{author_like}'")
                        cur.close()
                        con.commit()
                else:
                    add_new_author_like = Comment_discuss_comments_like(author_like = author_like, discuss_comment_id = comment_id_second, date_like = datetime.now(), down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    cur.execute(f"Select like_up, like_down from Comment_discuss_comments where id = {comment_id_second}")
                    results = cur.fetchall()
                    cur.execute(f'Update Comment_discuss_comments set like_up = {results[0][0] - 0}, like_down = {results[0][1] + 1} where id = {comment_id_second}')
                    con.commit()
            else:
                return 'Erorr'
        else:
            flash(f'Только авторизованные пользователи могут оставлять голоса')
        