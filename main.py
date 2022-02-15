from flask import Flask, render_template, request
import numpy as np
import spacy
import pickle
import re
import json
import random 

from datetime import datetime

import sqlite3

PORT_NUM = -1 # insert your port number here



with open('./example.json', 'r') as f:
    examples = json.load(f)

MAX_ANNOTATIONS=3
DATABASE_NAME = 'annotations.db'

s_dict = {} # sample dict, id => sample
a_dict = {} # annotation dict, id => list of (annotator, annotation)

a = {
        'Nichts': 'x',
        'Antimetabole': 'a',
        'Chiasmus': 'c'
        }

# get users
users = []
with open('users.txt', 'r') as f:
    users = []
    for l in f:
        uname = l.strip()
        if len(uname) == 5:
            users.append(uname)


print("start app...")
app = Flask(__name__)

for s in examples:
    sid = s['id']
    s_dict[sid] = s
    a_dict[sid] = []

def get_sid(user_name):
    print("get new sid for user", user_name)
   
    # get list of samples
    sids = []
    for s in s_dict:
        sids.append(s)

    # get list of annotations
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.execute("SELECT sid, name, annotation from ANNOTATIONS")
    annlist = [c for c in cursor]
    conn.close()

    # put annotations into dict
    print("going through database annotations...")
    ann_dict = {}
    for a in annlist:
        name = a[1]
        sid = a[0]

        if not sid in ann_dict:
            ann_dict[sid] = []

        ann_dict[sid].append(name)

    print(ann_dict)

    # remove sids where user has already annotated and where there are enough annotations
    sids_new = []
    for s in sids:
        if s not in ann_dict:
            ann_dict[s] = []

        if user_name not in ann_dict[s] and len(ann_dict[s]) < MAX_ANNOTATIONS:
            sids_new.append(s)
    sids = sids_new

    # choose sid if possible
    print(len(sids), "candidates to choose from")
    if len(sids) == 0:
        return None, None
    return random.choice(sids), len(sids)

def save_annotation(user_name, sid, annotation):
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute(f"INSERT INTO ANNOTATIONS (NAME, SID, ANNOTATION) VALUES ('{user_name}','{sid}','{annotation}')")

    if True:
        cursor = conn.execute("SELECT sid, name, annotation from ANNOTATIONS")
        for c in cursor:
            print(c)
    conn.commit()
    conn.close()




@app.route('/')
def index():
    random.seed(datetime.now())
    return render_template('index.html')


@app.route('/annotate', methods=['POST', 'GET'])
def annotate():
    user_name = request.form['uname'].strip()
    if user_name not in users: return(render_template('wrong_user.html', user_name=user_name))
    sid, remaining = get_sid(user_name)


    if sid is not None:
        text = s_dict[sid]['sentence']
        print(text)
        return render_template('annotate.html', chiasmus_content = text, user_name=user_name, sid=sid, num_sids = remaining)
    else:
        return render_template('done.html', user_name=user_name)

@app.route('/sub', methods=['POST', 'GET'])
def sub():
    user_name = request.form['uname'].strip()
    if user_name not in users: return(render_template('wrong_user.html', user_name=user_name))
    sid = request.form['sid']
    choice = request.form['choice']

    print("show sub with sid", sid, "and choice", choice, "for user", user_name)
    save_annotation(user_name, sid, choice)

    return render_template('sub.html', user_name=user_name, sid=sid, choice=choice)

@app.route('/datenschutz')
def datenschutz():
    return render_template('datenschutz.html')

@app.route('/impressum')
def impressum():
    return render_template('impressum.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=PORT_NUM)
