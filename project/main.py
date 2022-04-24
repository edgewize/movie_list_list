# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import FilmList
from .utils import buildList

main = Blueprint("main", __name__)


@main.route("/")
def index():
    all_lists = FilmList.query.all()
    for i in range(0, len(all_lists)):
        all_lists[i] = buildList(all_lists[i].id)
    return render_template(
        "index.html", data=all_lists, is_authenticated=current_user.is_authenticated
    )


@main.route("/film-list/<list_id>")
def list(list_id):
    data = buildList(list_id)
    return render_template("list.html", data=data, anon_user=current_user.is_anonymous)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)
