# coding=utf-8

from . import Base
from sqlalchemy import Column, String, Integer

class Biosequence(Base):
    __tablename__ = 'biosequence'

    bioentry_id = Column(Integer, primary_key=True)
    version = Column(Integer)
    length = Column(Integer)
    alphabet = Column(String(10))
    seq = Column(String)


    def __init__(self, bioentry_id, version, length, alphabet, seq):
        self.bioentry_id = bioentry_id
        self.version = version
        self.length = length
        self.alphabet = alphabet
        self.seq = seq

    def serialize(self):
        return {
            'bioentry_id':bioentry_id,
            'version':version,
            'length':length,
            'alphabet':alphabet,
            'seq':seq
        }
