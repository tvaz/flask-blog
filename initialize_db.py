from db import db, Post, sqlite_url
db.drop_all()
db.create_all()
