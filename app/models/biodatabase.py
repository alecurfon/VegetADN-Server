from app import db

class Biodatabase(db.Model):
    __tablename__ = 'biodatabase'
    __table_args__ = {'autoload':True}

    def match(self, str):
        tsvector = db.func.to_tsvector('simple', self.__str__(self))
        # from sqlalchemy import Index
        # index = Index('idx_biodb_fts', tsvector, postgresql_using='gin')
        str = str.strip()
        str = " ".join(str.split()).replace(' ', ' & ')
        print(f'QUERY: {str}')
        res = tsvector.match(str)
        return res

    def serialize(self):
        return {
            'biodatabase_id': self.biodatabase_id,
            'name': self.name,
            'authority': self.authority,
            'description': self.description
        }

    def __str__(self):
        return f'{self.name} {self.authority} {self.description}'
