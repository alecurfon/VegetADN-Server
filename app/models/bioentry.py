# coding=utf-8

from . import Base
from sqlalchemy import Column, String, Integer

class Bioentry(Base):
    __tablename__ = 'bioentry'

    bioentry_id = Column(Integer, primary_key=True)
    biodatabase_id = Column(Integer)
    taxon_id = Column(Integer)
    name = Column(String(40))
    accession = Column(String(128))
    identifier = Column(String(40))
    division = Column(String(6))
    desciption = Column(String)
    version = Column(Integer)

    def __init__(self, bioentry_id, biodatabase_id, taxon_id, name,
        accession, identifier, division, desciption, version):
            self.bioentry_id = bioentry_id
            self.biodatabase_id = biodatabase_id
            self.taxon_id = taxon_id
            self.name = name
            self.accession = accession
            self.identifier = identifier
            self.division = division
            self.desciption = desciption
            self.version = version

    def serialize(self):
        return {
            'bioentry_id':bioentry_id,
            'biodatabase_id':biodatabase_id,
            'taxon_id':taxon_id,
            'name':name,
            'accession':accession,
            'identifier':identifier,
            'division':division,
            'desciption':desciption,
            'version':version
        }
