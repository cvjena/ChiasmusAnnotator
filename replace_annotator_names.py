import secrets
import string
import os
import sqlite3

conn = sqlite3.connect('annotations.db')
cursor = conn.execute("SELECT sid, name, annotation from ANNOTATIONS")
lines = [c for c in cursor]
conn.close()

names = list(set([l[1] for l in lines]))


def generate_new_name(num_chars, existing_names):
    name = ''.join(secrets.choice(string.ascii_letters) for _ in range(num_chars))
    while name in existing_names:
        name = ''.join(secrets.choice(string.ascii_letters) for _ in range(num_chars))
    
    return name

name_dict = {}

names_new = []

for n in names:
    new = generate_new_name(10, names_new)
    names_new.append(new)
    name_dict[n] = new

lines_new = []
for l in lines:
    sid = l[0]
    name = l[1]
    annotation = l[2]
    name_new = name_dict[name]
    lines_new.append((sid, name_new, annotation))

for l, ln in zip(lines, lines_new):
    print(l, ln)

conn = sqlite3.connect('annotations-anonymous.db')
for l in lines_new:
    sid = l[0]
    user_name = l[1]
    annotation = l[2]
    conn.execute(f"INSERT INTO ANNOTATIONS (NAME, SID, ANNOTATION) VALUES ('{user_name}','{sid}','{annotation}')")
conn.commit()
conn.close()

