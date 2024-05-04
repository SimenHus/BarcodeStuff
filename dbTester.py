import atexit

import json
from database import DatabaseHandler
from common import *

db = DatabaseHandler(DATABASE_FOLDER)
db.connect()

with open(path.join(DATABASE_FOLDER, 'example.json')) as f:
    ex = json.load(f)

db.insert(ex)

items = db.fetch()

for item in items:
    print(item)


atexit.register(db.disconnect)