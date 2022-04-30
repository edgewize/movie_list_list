from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from .models import FilmList
from .utils import getListById, searchFilms, getListById, buildList
from . import db
import datetime

crud = Blueprint("crud", __name__)


@crud.route("/admin/create", methods=["GET", "POST"])
@login_required
def create():
    new_list = None
    if "title" in request.form:
        new_list = FilmList(
            title=request.form.get("title"),
            description=request.form.get("description"),
            created_at=datetime.datetime.now().date(),
        )
        db.session.add(new_list)
        db.session.commit()
        return redirect(f"/film-list/{new_list.id}")
    else:
        return render_template("create.html")


@crud.route("/admin/add/<list_id>", methods=["GET", "POST"])
@login_required
def add(list_id):
    film_list = getListById(list_id)
    if request.form.get("search"):
        search_result = searchFilms(request.form.get("search"))
        return render_template(
            "search_result.html", data=film_list, results=search_result
        )
    elif request.args.get("selection"):
        add_id = request.args.get("selection")
        if film_list.film_list:
            add_str = film_list.film_list + str(f", {add_id}")
        else:
            add_str = str(add_id)
        film_list.film_list = add_str
        db.session.commit()
        return redirect(f"/film-list/{list_id}", code=302)
    else:
        return render_template("search.html", data=film_list)


@crud.route("/admin/remove/<list_id>", methods=["GET", "POST"])
@login_required
def remove_list(list_id):
    data = buildList(list_id)
    return render_template("remove.html", data=data)


@crud.route("/admin/remove/<list_id>/<film_id>", methods=["GET", "POST"])
@login_required
def remove(list_id, film_id):
    film_list = getListById(list_id)
    working_list = [i.strip() for i in film_list.film_list.split(",")]
    working_list.remove(film_id)
    film_list.film_list = ",".join(working_list)
    db.session.commit()
    return redirect(f"/film-list/{list_id}", code=302)


@crud.route("/admin/edit/<list_id>", methods=["GET", "POST"])
@login_required
def edit(list_id):
    film_list = getListById(list_id)
    update = False
    if request.form.get("title"):
        film_list.title = request.form.get("title")
        db.session.commit()
        update = True
    if request.form.get("description"):
        film_list.description = request.form.get("description")
        update = True
    if update:
        return redirect(f"/film-list/{list_id}", code=302)
    else:
        return render_template(
            "create.html",
            data=film_list,
            action=f"/admin/edit/{list_id}",
            response=None,
        )


@crud.route("/admin/delete/<list_id>")
@login_required
def delete(list_id):
    item = getListById(list_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(f"/", code=302)
