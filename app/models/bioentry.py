# coding=utf-8

from . import db

class Bioentry(db.Model):
    __tablename__ = 'bioentry'

    bioentry_id = db.Column(db.Integer, primary_key=True)
    biodatabase_id = db.Column(db.Integer)
    taxon_id = db.Column(db.Integer)
    name = db.Column(db.String(40))
    accession = db.Column(db.String(128))
    identifier = db.Column(db.String(40))
    division = db.Column(db.String(6))
    description = db.Column(db.String)
    version = db.Column(db.Integer)

    # def __init__(self, bioentry_id, biodatabase_id, taxon_id, name,
    #     accession, identifier, division, description, version):
    #         self.bioentry_id = bioentry_id
    #         self.biodatabase_id = biodatabase_id
    #         self.taxon_id = taxon_id
    #         self.name = name
    #         self.accession = accession
    #         self.identifier = identifier
    #         self.division = division
    #         self.description = description
    #         self.version = version

    def serialize(self):
        return {
            'bioentry_id':self.bioentry_id,
            'biodatabase_id':self.biodatabase_id,
            'taxon_id':self.taxon_id,
            'name':self.name,
            'accession':self.accession,
            'identifier':self.identifier,
            'division':self.division,
            'description':self.description,
            'version':self.version
        }
