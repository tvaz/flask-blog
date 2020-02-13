from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return 'Post: "{}"'.format(self.title)
#db.create_all()

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route('/new')
def create():
    return index()

@app.route('/delete/<id>')
def delete(id):
    return index()

@app.route('/edit/<id>')
def update(id):
    return index()
