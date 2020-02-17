from flask import Blueprint, render_template, redirect, request, url_for, flash
from webapp.model import db, Users, Comment, Profile, Gallary, Discussion
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
import os, shutil

blueprint = Blueprint('my_profile_engraver', __name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'JPG', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


#@blueprint.route('/add-photo-in-gallary', methods = ['POST'])


@blueprint.route('/additional-profile-information', methods = ['POST'])
def additional_profile_information():
    if redirect.method == 'POST':
        return True

