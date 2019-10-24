from app import db

class Biosequence(db.Model):
    __tablename__ = 'biosequence'
    __table_args__ = {'autoload':True}

    def serialize(self):
        return {
            'bioentry_id':self.bioentry_id,
            'version':self.version,
            'length':self.length,
            'alphabet':self.alphabet,
            'seq':self.seq
        }

    def __str__(self):
        return f'{self.version} {self.length} {self.alphabet} {self.seq}'
