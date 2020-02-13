from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, validators

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

class NewPostForm(Form):
    title = StringField('Title', [validators.length(min=1, max=120)])
    body = StringField('Body', [validators.length(min=1, max=2000)]) 

@app.route('/')
def index():
    posts = Post.query.all()
    print(posts)
    return render_template("index.html", posts=posts)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    form = NewPostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("new.html", form=form)

@app.route('/create')
def create():
    return index()

@app.route('/delete/<id>')
def delete(id):
    return index()

@app.route('/edit/<id>')
def update(id):
    return index()
