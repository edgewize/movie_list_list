from project import db, create_app, models
import datetime

db.create_all(app=create_app())

first_list = models.FilmList(
    title="First Movie List",
    description="A fun collection of favorite films",
    created_at=datetime.datetime.now().date(),
    film_list="218,348",
)
db.session.add(first_list)
db.session.commit()
