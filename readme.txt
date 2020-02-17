set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
export FLASK_APP=webapp && export FLASK_ENV=development && flask run


set FLASK_APP=webapp && flask shell

pip freeze > requirements.txt



set FLASK_APP=webapp && FLASK db init
move webdb.db webdb.db.old
set FLASK_APP && flask db migrate -m "add new table commet comments"
flask db upgrade
move webdb.db.old webdb.db
flask db stamp de08b25fb416




<link href="{{ url_for('static' , filename='css/style_css_header.css') }}" rel='stylesheet'>
    <link href="{{ url_for('static' , filename='css/style_css_content.css') }}" rel='stylesheet'>
    <link href="{{ url_for('static' , filename='css/registration.css') }}" rel='stylesheet'>
    <link href="{{ url_for('static' , filename='css/style_css_main_page.css') }}" rel='stylesheet'>
    <link href="{{ url_for('static' , filename='css/style_css_profile_engraver.css') }}" rel='stylesheet'>
    <link href="{{ url_for('static' , filename='css/style_css_login_profile_engraver.css') }}" rel='stylesheet'>

https://ru.freepik.com/free-icons/2  
https://www.pinterest.ru/           				------Иконки
Гравировка бывает:
-На металле
-На пластике
-На дереве
-На стекле
-На коже


Поднятие ssh сервера на virtual box 
https://phoenixnap.com/kb/how-to-enable-ssh-centos-7
Команды Linux


width, height = im.size 
  
# Setting the points for cropped image 
left = 5
top = height / 4
right = 164
bottom = 3 * height / 4
  
# Cropped image of above dimension 
# (It will not change orginal image) 
im1 = im.crop((left, top, right, bottom)) 
  
# Shows the image in image viewer 
im1.show()




if current_user.is_authenticated:
        discuss_id = request.args.get('id')
        like = request.args.get('like')
        name_discuss = request.args.get('name_discuss')
        author_like = current_user.login
        if like == 'like_up':
            cur = con.cursor()
            cur.execute(f"Select like_up, like_down from Discussion where id = {discuss_id}")
            results = cur.fetchall()
            if results[0][0] == None and results[0][1] == None:
                cur.execute(f'Update Discussion set like_up = 1, like_down = 0 where id = {discuss_id}')
                con.commit()
                cur.execute(f"Update Discussion_like set up = 1, down = 0 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                cur.close()
                con.commit()
                author_like_exist = Discussion_like.query.filter_by(discuss_id = discuss_id, author_like = author_like).first()
                if not author_like_exist:
                    add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, down = 0, up = 1)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    return redirect(url_for('discussions.discussion'))

            author_like_exist = Discussion_like.query.filter_by(discuss_id = discuss_id, author_like = author_like).first()
            if author_like_exist and results[0][0] != None and results[0][1] != None:
                cur.execute(f"select up, down from Discussion_like where discuss_id = {discuss_id} and author_like = '{author_like}'")
                answer = cur.fetchall()
                if answer[0][0] == 1:
                    flash(f"Вы уже проголосовали за эту запись")
                    return redirect(url_for('discussions.discussion'))
                elif answer[0][0] == 0:
                    cur.execute(f'Update Discussion set like_up = {results[0][0] + answer[0][1]}, like_down = {results[0][1] - answer[0][1]} where id = {discuss_id}')
                    con.commit()
                    cur.execute(f"Update Discussion_like set up = 1, down = 0 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                    cur.close()
                    con.commit()
                    return redirect(url_for('discussions.discussion'))
            else:
                add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, down = 0, up = 1)
                db.session.add(add_new_author_like)
                db.session.commit()
                cur.execute(f'Update Discussion set like_up = {results[0][0] + 1}, like_down = {results[0][1] - 0} where id = {discuss_id}')
                con.commit()
                cur.execute(f"Update Discussion_like set up = 1, down = 0 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                cur.close()
                con.commit()
                return redirect(url_for('discussions.discussion'))

        elif like == 'like_down':
            cur = con.cursor()
            cur.execute(f"Select like_down, like_up from Discussion where id = {discuss_id}")
            results = cur.fetchall()
            if results[0][0] == None and results[0][1] == None:
                cur.execute(f'Update Discussion set like_down = 1, like_up = 0 where id = {discuss_id}')
                con.commit()
                cur.execute(f"Update Discussion_like set up = 0, down = 1 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                cur.close()
                con.commit()
                if not author_like_exist:
                    add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, down = 1, up = 0)
                    db.session.add(add_new_author_like)
                    db.session.commit()
                    return redirect(url_for('discussions.discussion')) 

            author_like_exist = Discussion_like.query.filter_by(discuss_id = discuss_id, author_like = author_like).first()
            if author_like_exist and results[0][0] != None and results[0][1] != None:
                cur.execute(f"select down, up from Discussion_like where discuss_id = {discuss_id} and author_like = '{author_like}'")
                answer = cur.fetchall()
                if answer[0][0] == 1:
                    flash(f"Вы уже проголосовали за эту запись")
                    return redirect(url_for('discussions.discussion'))
                elif answer[0][0] == 0:
                    cur.execute(f'Update Discussion set like_down = {results[0][0] + answer[0][1]}, like_up = {results[0][1] - answer[0][1]} where id = {discuss_id}')
                    con.commit()
                    cur.execute(f"Update Discussion_like set up = 0, down = 1 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                    cur.close()
                    con.commit()
                    return redirect(url_for('discussions.discussion'))
            else:
                add_new_author_like = Discussion_like(author_like = author_like, discuss_id = discuss_id, down = 0, up = 1)
                db.session.add(add_new_author_like)
                db.session.commit()
                cur.execute(f'Update Discussion set like_down = {results[0][0] + 1}, like_up = {results[0][1] - 0} where id = {discuss_id}')
                con.commit()
                cur.execute(f"Update Discussion_like set down = 1, up = 0 where discuss_id = {discuss_id} and author_like = '{author_like}'")
                cur.close()
                con.commit()
                return redirect(url_for('discussions.discussion'))
        else:
            return redirect(url_for('discussions.discussion'))
    else:
        flash(f'Только авторизованные пользователи могут оставлять голоса')
        return redirect(url_for('discussions.discussion'))