from flask import Flask, render_template, request, redirect, url_for
from forms import NewPostForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Post(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Post: "{}"'.format(self.title)

db.create_all()

@app.route('/')
def index():
    posts = Post.query.all()
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

@app.route('/del/<id>')
def delete(id):
    post = Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.filter_by(id=id).one()
    form = NewPostForm(obj=post)

    if request.method == 'POST':
        form = NewPostForm(request.form)
        if form.validate():
            post.title = form.title.data
            post.body = form.body.data
            db.session.commit()
            return redirect(url_for('index'))

    return render_template("edit.html", form=form)
