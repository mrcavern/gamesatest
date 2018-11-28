import os
from config import db
from models import Person

# Data to initialize database with
PEOPLE = [
    {"fname": "David", "lname": "Cuevas"},
    {"fname": "Demo", "lname": "User"},
    {"fname": "Last", "lname": "User"},
]

# Delete database file if it exists currently
if os.path.exists("people.db"):
    os.remove("people.db")

# Create the database
db.create_all()

# iterate over the PEOPLE structure and populate the database
for person in PEOPLE:
    p = Person(lname=person.get("lname"), fname=person.get("fname"))
    db.session.add(p)

db.session.commit()
