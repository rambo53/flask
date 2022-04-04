import datetime, re
from telnetlib import STATUS
from app import db, login_manager, Bcrypt

#fonction pour formater nos url en lower case et avec un '-' à la place des espaces
def slugify(s):
    return re.sub('[^\w]+','-',s).lower()

entry_tags = db.Table('entry_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1

    id = db.Column(db.Integer, primary_key=True)
    title =  db.Column(db.String(100))
    slug =  db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    tags = db.relationship('Tag', secondary=entry_tags, backref=db.backref('entries', lazy='dynamic'))

    #constructeur
    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Entry : %s>' %self.title


#différente classe     

class Tag(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100))
    slug =  db.Column(db.String(100), unique=True)

    #constructeur
    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag : %s>' %self.name


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(100))
    email =  db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255))
    slug = db.Column(db.String(100), unique=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    active = db.Column(db.Boolean, default=True)

    #constructeur
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return '<User : %s>' %self.name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
    
    def is_active(self):
        return self.active
    
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    #crée mon password haché
    @staticmethod
    def make_password(password):
        return Bcrypt.generate_password_hash(password)
    
    #vérifie la concordance entre le password qui est envoyé et celui stocké pour mon utilisateur
    def check_password(self, raw_password):
        return Bcrypt.check_password_hash(self.password_hash, raw_password)
    
    @classmethod
    def create(cls, email, password, **kwargs):
        return User(
            email=email,
            password_hash = User.make_password(password),
            **kwargs
        )

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter(User.email == email).first()
        if user and user.check_password(password):
            return user
        return False


#pour récupérer l'id de mon user à travers mon appli
@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))