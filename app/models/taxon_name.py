# coding=utf-8

from . import db

class TaxonName(db.Model):
    __tablename__ = 'taxon_name'

    taxon_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    name_class = db.Column(db.String(32))

    # def __init__(self, name, name_class):
    #     self.name = name
    #     self.name_class = name_class

    def serialize(self):
        return {
            'taxon_id':self.taxon_id,
            'name':self.name,
            'name_class':self.name_class
        }
