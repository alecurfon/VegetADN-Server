# coding=utf-8

from . import Base
from sqlalchemy import Column, String, Integer

class TaxonName(Base):
    __tablename__ = 'taxon_name'

    taxon_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    name_class = Column(String(32))

    def __init__(self, name, name_class):
        self.name = name
        self.name_class = name_class

    def serialize(self):
        return {
            'taxon_id':taxon_id,
            'name':name,
            'name_class':name_class
        }
