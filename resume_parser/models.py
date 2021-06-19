from sqlalchemy.orm import backref
from resume_parser import db


class Resume(db.Model):
    __tablename__='resume'
    id = db.Column(db.String, primary_key=True)
    location=db.Column(db.String)
    email=db.relationship('Email',backref='resume')
    mobile=db.relationship('Mobile',backref='resume')


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String)
    resume_id=db.Column(db.String,db.ForeignKey('resume.id'))
class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mobile=db.Column(db.String)
    resume_id=db.Column(db.String,db.ForeignKey('resume.id'))

