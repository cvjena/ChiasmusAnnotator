import sqlite3

print_name = True

conn = sqlite3.connect('annotations-anonymous.db')

cursor = conn.execute("SELECT sid, name, annotation from ANNOTATIONS")
lines = [c for c in cursor]
conn.close()

sids = {}

nann = {}

for l in lines: 
    sid = l[0]
    name = l[1]
    annotation = l[2]

    if not name in nann:
        nann[name] = 0

    nann[name] += 1

for n in nann:
    print(n, "-", nann[n])
