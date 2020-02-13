from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

sqlite_url = 'sqlite:///posts.sqlite3'

app.config['SQLALCHEMY_DATABASE_URI'] = sqlite_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Post: "{}"'.format(self.title)
