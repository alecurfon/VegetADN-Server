# coding=utf-8

from . import db

class Biosequence(db.Model):
    __tablename__ = 'biosequence'

    bioentry_id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer)
    length = db.Column(db.Integer)
    alphabet = db.Column(db.String(10))
    seq = db.Column(db.String)


    # def __init__(self, bioentry_id, version, length, alphabet, seq):
    #     self.bioentry_id = bioentry_id
    #     self.version = version
    #     self.length = length
    #     self.alphabet = alphabet
    #     self.seq = seq

    def serialize(self):
        return {
            'bioentry_id':self.bioentry_id,
            'version':self.version,
            'length':self.length,
            'alphabet':self.alphabet,
            'seq':self.seq
        }
