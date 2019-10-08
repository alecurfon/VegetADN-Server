# coding=utf-8

from . import db

class Biodatabase(db.Model):
    __tablename__ = 'biodatabase'

    biodatabase_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    authority = db.Column(db.String(128))
    description = db.Column(db.String)


    # def __init__(self, name, authority, description):
    #     self.name = name
    #     self.authority = authority
    #     self.description = description

    def serialize(self):
        return {
            'biodatabase_id': self.biodatabase_id,
            'name': self.name,
            'authority': self.authority,
            'description': self.description
        }
