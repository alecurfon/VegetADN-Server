# coding=utf-8

from . import Base
from sqlalchemy import Column, String, Integer

class Biodatabase(Base):
    __tablename__ = 'biodatabase'

    biodatabase_id = Column(Integer, primary_key=True)
    name = Column(String(128))
    authority = Column(String(128))
    description = Column(String)


    def __init__(self, name, authority, description):
        self.name = name
        self.authority = authority
        self.description = description

    def serialize(self):
        return {
            'biodatabase_id': self.biodatabase_id,
            'name': self.name,
            'authority': self.authority,
            'description': self.description
        }
