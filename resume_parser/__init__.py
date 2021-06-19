from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app =Flask(__name__)
app.config['SECRET_KEY']='mysecret'
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
if os.getenv('testing')=='true':
    print("TESTING MODE")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir,'data_test.sqlite')
db=SQLAlchemy(app)
import resume_parser.models


db.create_all()
db.session.commit()
from resume_parser.core.views import core
app.register_blueprint(core)