from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

db = SQLAlchemy()



class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String, unique = False, nullable = False)
    status = db.Column(db.String, unique = False, nullable = True)
    first_name = db.Column(db.String(50) ,unique = False, nullable = False)
    second_name = db.Column(db.String(50),unique = False, nullable = False)
    login = db.Column(db.String(50), unique = True, nullable = False, index = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    images = db.Column(db.String(250), unique = False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __init__(self, login,first_name, second_name, email, images, role, status):
        self.second_name = second_name
        self.first_name = first_name
        self.login = login
        self.email = email
        self.images = images
        self.role = role
        self.status = status

    def __repr__(self):
        return f'{self.login}'


class Profile(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    first_name = db.Column(db.String(50) ,unique = False, nullable = False)
    second_name = db.Column(db.String(50),unique = False, nullable = False)
    login = db.Column(db.String(50), unique = True, nullable = False, index = True)
    city = db.Column(db.String(250), unique = False, nullable = True)
    region = db.Column(db.String(250), unique = False, nullable = True)
    brifdate = db.Column(db.String(20), unique = False, nullable = True)  
    work_profile = db.Column(db.String(250), unique = False, nullable = True)
    experience = db.Column(db.String(250), unique = False, nullable = True)
    link_you_tube = db.Column(db.String(250), unique = True, nullable = True)
    link_you_instagram = db.Column(db.String(250), unique = True, nullable = True)
    link_you_vkontakte = db.Column(db.String(250), unique = True, nullable = True)
    about_himsefl_profile = db.Column(db.Text, unique = False, nullable = True)
    info_profile_login = db.Column(db.String, unique = True, nullable = True)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id',  ondelete = 'CASCADE'), unique = True, index = True)

    def __repr__(self):
        return f'{self.owner_id}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_reciver = db.Column(db.String, nullable=False)
    user_author = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True)

    user = relationship('Users', backref='comments')

    def __repr__(self):
        return '<Comment {}>'.format(self.id)


class Gallary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_photo = db.Column(db.String(250), unique = False, nullable = True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_author_login = db.Column(db.String(250), unique = False, nullable = False)

    user_author = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True)
    user = relationship('Users', backref='gallaries')

    def __repr__(self):
        return f'{self.name_photo}, {self.user_author_login}'

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name_discuss = db.Column(db.String(250), unique = True, nullable = True)
    author_discuss = db.Column(db.Integer, unique = False, nullable = True)
    author_discuss_login = db.Column(db.String(250), unique = False, nullable = True)
    created_discuss = db.Column(db.DateTime, nullable=False)
    like_up = db.Column(db.Integer, unique = False, nullable = True)
    like_down = db.Column(db.Integer, unique = False, nullable = True)

    def __repr__(self):
        return f'{self.author_discuss_login}'

class Discussion_like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_like = db.Column(db.String, unique = False, nullable = False)
    date_like = db.Column(db.DateTime,unique = False, nullable=False)
    up = db.Column(db.Integer, unique = False, nullable = True)
    down = db.Column(db.Integer, unique = False, nullable = True)

    discuss_id = db.Column(db.Integer, db.ForeignKey('discussion.id', ondelete='CASCADE'), index=True)

    def __repr__(self):
        return f'{self.discuss_id}'


class Discuss_comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    discuss_comment_created = db.Column(db.DateTime, nullable = False, default = datetime.now())
    user_login = db.Column(db.String(250), unique = False, nullable = True)
    like_up = db.Column(db.Integer, unique = False, nullable = True)
    like_down = db.Column(db.Integer, unique = False, nullable = True)

    discuss_id = db.Column(db.Integer, db.ForeignKey('discussion.id', ondelete='CASCADE'), index=True)

    def __repr__(self):
        return f'{self.id}'


class Discuss_comments_like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_like = db.Column(db.String, unique = False, nullable = False)
    date_like = db.Column(db.DateTime,unique = False, nullable=False)
    up = db.Column(db.Integer, unique = False, nullable = True)
    down = db.Column(db.Integer, unique = False, nullable = True)

    discuss_comment_id = db.Column(db.Integer, db.ForeignKey('discuss_comments.id', ondelete='CASCADE'), index=True)

    def __repr__(self):
        return f'{self.discuss_id}'


class Comment_discuss_comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False)
    user_login = db.Column(db.String, unique = False, nullable = True)
    like_up = db.Column(db.Integer, unique = False, nullable = True)
    like_down = db.Column(db.Integer, unique = False, nullable = True)

    discuss_comment_id = db.Column(db.Integer, db.ForeignKey('discuss_comments.id', ondelete = 'CASCADE'), index = True)

    def __repr__(self):
        return f'{self.discuss_comment_id}'


class Comment_discuss_comments_like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_like = db.Column(db.String, unique = False, nullable = False)
    date_like = db.Column(db.DateTime,unique = False, nullable=False)
    up = db.Column(db.Integer, unique = False, nullable = True)
    down = db.Column(db.Integer, unique = False, nullable = True)

    discuss_comment_id = db.Column(db.Integer, db.ForeignKey('comment_discuss_comments.id', ondelete='CASCADE'), index=True)

    def __repr__(self):
        return f'{self.discuss_id}'


class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    event_name = db.Column(db.String, unique = False, nullable = False)
    event_type = db.Column(db.String, unique = False, nullable = False)
    event_prev_text_first = db.Column(db.String, unique = False, nullable = False)
    event_prev_text_second = db.Column(db.String, unique = False, nullable = False)
    event_text = db.Column(db.Text, nullable = False)
    event_created = db.Column(db.DateTime, nullable = False, default = datetime.now())
    event_author_login = db.Column(db.String, unique = False, nullable = False)

    def __repr__(self):
        return f'{self.event_name}'


class Topic_event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    topic_event_created = db.Column(db.DateTime, nullable = False, default = datetime.now())
    topic_event_name = db.Column(db.String(150), unique = False, nullable = False)
    topic_event_author = db.Column(db.String(50), unique = False, nullable = False)
    topic_event_limitations = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_one = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_two = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_three = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_four = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_five = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_six = db.Column(db.String, unique = False, nullable = True)
    topic_event_rule_seven = db.Column(db.String, unique = False, nullable = True)
    topic_event_prerequisites = db.Column(db.Text, unique = False, nullable = True)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), index=True)

    def __repr__(self):
        return f'{self.topic_event_name}'


class Photo_event(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    first_photo = db.Column(db.String, nullable = True, unique = False)
    second_photo = db.Column(db.String, nullable = True, unique = False)
    three_photo = db.Column(db.String, nullable = True, unique = False)
    author_photo = db.Column(db.String, nullable = True, unique = False)
    voice = db.Column(db.Integer, nullable = True, unique = False)
    cast_a_vote = db.Column(db.String, nullable = True, unique = False)
    topic_event_id_photo = db.Column(db.Integer, nullable = False, unique = False)
    like_up = db.Column(db.Integer, unique = False, nullable = True)
    like_down = db.Column(db.Integer, unique = False, nullable = True)

    photo_event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), index=True)

    def __repr__():
        return f'{self.author_photo}'

class Photo_event_like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_like = db.Column(db.String, unique = False, nullable = False)
    date_like = db.Column(db.DateTime,unique = False, nullable=False)
    up = db.Column(db.Integer, unique = False, nullable = True)
    down = db.Column(db.Integer, unique = False, nullable = True)

    like_photo_id = db.Column(db.Integer, db.ForeignKey('photo_event.id', ondelete='CASCADE'), index=True)

    def __repr__(self):
        return f"{self.id}"