from flask import Blueprint, render_template, redirect, request
from webapp.model import db, Users, Discussion, Profile
import paginate

blueprint = Blueprint('all_pofile_blueprint', __name__)

@blueprint.route('/all-profile/')
def all_profiles():
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
        
    user = Users.query
    engravers_pages = user.paginate( page = page, per_page = 50)
    dop_info = Profile.query.filter(Profile.city != '').all()
    return render_template('users/all_engraver_profile.html', engravers_pages = engravers_pages, page =page, dop_info = dop_info)


