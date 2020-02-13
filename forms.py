from wtforms import Form, StringField, validators

class NewPostForm(Form):
    title = StringField('Title', [validators.length(min=1, max=120)])
    body = StringField('Body', [validators.length(min=1, max=2000)])
