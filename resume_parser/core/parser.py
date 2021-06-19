import sys
import subprocess
import re
import os
from werkzeug.utils import secure_filename
import fitz  # this is pymupdf


def convert_to(folder, source, timeout=None):
    print("Source is,",source)
    args = [libreoffice_exec(), '--headless', '--convert-to', 'pdf', '--outdir', folder, source]

    process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Output of the command is ",process.stdout.decode())
    filename = re.search('-> (.*?) using filter', process.stdout.decode())

    if filename is None:
        raise LibreOfficeError(process.stdout.decode())
    else:
        return filename.group(1)


def libreoffice_exec():

    return 'libreoffice7.1'


class LibreOfficeError(Exception):
    def __init__(self, output):
        self.output = output



def save_to(folder, file):
    os.makedirs(folder, exist_ok=True)
    save_path = os.path.join(folder, secure_filename(file.filename))
    file.save(save_path)
    print("Save path is, ",save_path)
    return save_path




def getPDFText(file_name):
    with fitz.open(file_name) as doc:
        text = ""
        for page in doc:
            text += page.getText()
    return text


def extractInfo(pdfText):
    pattern=re.compile('(\\+91)?(-)?\\s*?(91)?\\s*?(\\d{3})-?\\s*?(\\d{3})-?\\s*?(\\d{4})')
    mobile_numbers=re.findall(pattern,pdfText)
    mobile_numbers=[''.join(a) for a in mobile_numbers]
    pattern='([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
    emails=re.findall(pattern,pdfText)
    emails=[''.join(a) for a in emails]
    return mobile_numbers,emails
