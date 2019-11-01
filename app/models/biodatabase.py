from app import db

class Biodatabase(db.Model):
    __tablename__ = 'biodatabase'
    __table_args__ = {'autoload':True}
    # from sqlalchemy import Index
    # index = Index('idx_biodb_fts', tsvector, postgresql_using='gin')

    def match(self, query):
        from app import db
        tsvector = db.func.to_tsvector(str(self))
        query = query.strip().split()
        query = ' & '.join(query)
        print(f'TSVECTOR: {tsvector}\nDOCUMENT: {str(self)}\nQUERY: {query}')
        return tsvector.match(query)

    def serialize(self):
        return {
            'biodatabase_id': self.biodatabase_id,
            'name': self.name,
            'authority': self.authority,
            'description': self.description
        }

    def __str__(self):
        return self.name + ' ' + \
            db.func.coalesce(self.authority, "") + ' ' + \
            db.func.coalesce(self.description, "")
