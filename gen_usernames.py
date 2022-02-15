import secrets
import string


def generate_new_name(num_chars, existing_names):
    name = ''.join(secrets.choice(string.ascii_letters) for _ in range(num_chars))
    while name in existing_names:
        name = ''.join(secrets.choice(string.ascii_letters) for _ in range(num_chars))
    
    return name

name_dict = {}

names_new = []

for n in range(30):
    new = generate_new_name(5, names_new)
    names_new.append(new)

with open('users.txt', 'w') as f:
    for n in names_new:
        f.write(n+"\n")
