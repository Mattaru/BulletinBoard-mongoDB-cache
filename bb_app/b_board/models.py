from django.db import models
from mongoengine import Document, fields


class Comment(Document):
    name = fields.StringField()
    text = fields.StringField()


class Post(Document):
    title = fields.StringField()
    text = fields.StringField()
    tags = fields.ListField()
    comments = fields.ListField()



