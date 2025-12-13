from app.db import db
from datetime import datetime

class Budget(db.Model):
    __tablename__= 'budget'
    id= db.column(db.integer,primary_key=True)
    