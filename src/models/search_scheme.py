from .. import db

class BiodatabaseSearch(db.Model):
    __tablename__ = 'biodatabase_search'
    __table_args__ = (
            db.PrimaryKeyConstraint('biodatabase_id'),
            {'extend_existing':True, 'autoload':True})

class BioentrySearch(db.Model):
    __tablename__ = 'bioentry_search'
    __table_args__ = (
            db.PrimaryKeyConstraint('bioentry_id'),
            {'extend_existing':True, 'autoload':True})

class TaxonSearch(db.Model):
    __tablename__ = 'taxon_search'
    __table_args__ = (
            db.PrimaryKeyConstraint('taxon_id'),
            {'extend_existing':True, 'autoload':True})
