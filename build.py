from project import db, create_app, models
import datetime

db.create_all(app=create_app())
