from flask.helpers import url_for

from werkzeug.utils import redirect
from resume_parser.core.parser import convert_to, extractInfo, save_to,getPDFText
from resume_parser.models import Resume,Email,Mobile
from flask import Blueprint, json,request,abort,jsonify,Response
from uuid import uuid4
import os
from resume_parser.config import config
from resume_parser import db
core=Blueprint('core',__name__)


def handle_upload(file):
    upload_id = str(uuid4())
    source = save_to(os.path.join(config['uploads_dir'], 'source', upload_id), file)
    
    try:
        result = convert_to(os.path.join(config['uploads_dir'], 'pdf', upload_id), source)
        print(result)
    except Exception as e:
        abort(500, description=e)
    pdfText=getPDFText(result)
    mobileNums,emails=extractInfo(pdfText)

    newResume=Resume(id=upload_id,location=result)
    for m in mobileNums:
        nM=Mobile(mobile=m)
        newResume.mobile.append(nM)
        db.session.add(nM)
    for e in emails:
        nE=Email(email=e)
        newResume.email.append(nE)
        db.session.add(nE)
    db.session.add(newResume)
    db.session.commit()
    return newResume



@core.route('/upload/',methods=['GET', 'POST'])
def upload_cv():
    ret=[]
    for file in request.files.getlist('files'):
        workingResume=handle_upload(file)
        mobiles,emails=get_info_cv(workingResume)
        ret.append({'id':workingResume.id,'mobile':mobiles,'email':emails})
    return jsonify(ret)



def get_info_cv(resumeInfo):
    mobiles=resumeInfo.mobile
    mobiles=[a.mobile for a in mobiles]
    mobiles=list(set(mobiles))
    emails=resumeInfo.email
    emails=[a.email for a in emails]
    emails=list(set(emails))

    return mobiles,emails


@core.route('/getinfo')
def get_info():
    id=request.args.get('id')
    if not id:
        abort(404,description="Please include id")
    resumeInfo=Resume.query.get_or_404(id)
    mobiles,emails=get_info_cv(resumeInfo)
    return jsonify({'id':id,'mobile':mobiles,'email':emails})
    

@core.route('/getAllExcel')
def get_excel():
    all_cv=Resume.query.all()
    resp="id,mobile,email\n"
    for resume in all_cv:
        mobiles,emails=get_info_cv(resume)
        resp+=str(resume.id)+","+'"'+','.join(mobiles)+'"'+','+'"'+','.join(emails)+'"'+'\n'
    return Response(resp,mimetype='text/csv',headers={"Content-disposition":
                 "attachment; filename=allResume.csv"})