from mongoengine import Document, StringField, ReferenceField, ListField, CASCADE
from mongoengine import connect

connect(
    db="web20",
    host="mongodb+srv://goitlearn:*******@goitlearn.w7mvfnf.mongodb.net/?retryWrites=true&w=majority&appName=goitlearn",
    tls=True,
    tlsInsecure=True,
)


class Author(Document):
    fullname = StringField(max_length=150, required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=100)
    description = StringField()
    meta = {"collection": 'authors'}


class Quote(Document):
    tags = ListField(StringField(max_length=300))
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": 'quotes'}