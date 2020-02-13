from wtforms import Form, StringField, TextAreaField, validators

class NewPostForm(Form):
    title = StringField('Title', [validators.length(min=1, max=120)])
    body = TextAreaField('Body', [validators.length(min=1, max=2000)])
