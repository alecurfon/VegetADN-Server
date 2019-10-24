from app import db

class Bioentry(db.Model):
    __tablename__ = 'bioentry'
    __table_args__ = {'autoload':True}

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

    def __str__(self):
        return f'{self.name} {self.accession} {self.identifier}' \
            f'{self.division} {self.description} {self.version}'
