"""
A simple implementation of a blogging application.

Tori Vaz 2020
"""

from flask import Flask, render_template, request, redirect, url_for
from forms import NewPostForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Post: "{}"'.format(self.title)

@app.route('/')
def index():
    """
    Main page for application. Shows a list of all posts.
    """
    posts = Post.query.all()
    return render_template("index.html", posts=posts)

@app.route('/post/<id>')
def post(id):
    """
    Shows details for a given post.
    """
    post = Post.query.filter_by(id=id).one()
    return render_template("post.html", post=post)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    """
    Creates a new post.
    """
    form = NewPostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(title=form.title.data, body=form.body.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("new.html", form=form)

@app.route('/del/<id>')
def delete(id):
    """
    Deletes a post and returns to the main page.
    """
    post = Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def update(id):
    """
    Updates the post and returns to the post details view.
    """
    post = Post.query.filter_by(id=id).one()
    form = NewPostForm(obj=post)

    if request.method == 'POST':
        form = NewPostForm(request.form)
        if form.validate():
            post.title = form.title.data
            post.body = form.body.data
            db.session.commit()
            return redirect(url_for('post', id=id))
    return render_template("edit.html", form=form)
