from app import db

class Bioentry(db.Model):
    __tablename__ = 'bioentry'
    __table_args__ = {'autoload':True}

    def match(self, query):
        from app import db
        tsvector = db.func.to_tsvector(str(self))
        query = query.strip().split()
        query = ' & '.join(query)
        print(f'TSVECTOR: {tsvector}\nDOCUMENT: {str(self)}\nQUERY: {query}')
        return tsvector.match(query)

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
        return ' '.join([self.name,
            self.accession,
            db.func.coalesce(self.identifier, ''),
            db.func.coalesce(self.division, ''),
            db.func.coalesce(self.description , ''),
            self.version])
