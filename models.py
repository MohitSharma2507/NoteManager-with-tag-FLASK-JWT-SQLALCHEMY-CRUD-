from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

note_tags = db.Table('note_tags',
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'), primary_key=True),
    db.Column('tag_id',  db.Integer, db.ForeignKey('tag.id'),  primary_key=True)
)

class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)                    # removed unique=True
    email    = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
 # One-to-many: one user has many notes
    notes = db.relationship('Note', backref='author', lazy=True , cascade='all, delete-orphan')          # backref='author'
  # One-to-many: one user has many tags 
    tags  = db.relationship('Tag',  backref='owner',  lazy=True, cascade='all, delete-orphan')          # backref='owner'

    def to_dict(self):
        return {
            'id':    self.id,
            'email': self.email
        }


class Note(db.Model):
    id         = db.Column(db.Integer, primary_key=True)                  # removed unique=True
    title      = db.Column(db.String(100), nullable=False)
    content    = db.Column(db.Text, nullable=True)
    is_pinned  = db.Column(db.Boolean, default=False)                           # Text not String(250)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id    = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tags = db.relationship('Tag', secondary=note_tags, backref='notes')

    def to_dict(self):
        return {
            'id':         self.id,
            'title':      self.title,
            'content':    self.content,
            'created_at': self.created_at.strftime('%d %b %Y %I:%M %p'), # formatted string
            'updated_at': self.updated_at.strftime('%d %b %Y %I:%M %p'), # formatted string
            'user_id':    self.user_id,
            'tags':       [t.to_dict() for t in self.tags],
            'is_pinned': self.is_pinned
        }

class Tag(db.Model):
    id      = db.Column(db.Integer, primary_key=True)                    
    name    = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

 # Unique constraint — same user can't have two tags with the same name
    __table_args__= (db.UniqueConstraint('name','user_id',name='unique_tag_per_user'),)


    def to_dict(self):
        return {
            'id':      self.id,
            'name':    self.name,
            'user_id': self.user_id
        }