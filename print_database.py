import sqlite3

print_name = True

conn = sqlite3.connect('annotations-anonymous.db')

cursor = conn.execute("SELECT sid, name, annotation from ANNOTATIONS")
lines = [c for c in cursor]
conn.close()

sids = {}


for l in lines: 
    sid = l[0]
    name = l[1]
    annotation = l[2]

    if not sid in sids:
        sids[sid] = []
    if print_name:
        sids[sid].append(annotation+'#'+name)
    else:
        sids[sid].append(annotation)

for s in sids:
    print(s,'-',sids[s])
