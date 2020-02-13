from flask import Flask, render_template, request, redirect, url_for
from db import db, Post
from forms import NewPostForm

app = Flask(__name__)

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
