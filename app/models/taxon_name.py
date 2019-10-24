from app import db

class TaxonName(db.Model):
    __tablename__ = 'taxon_name'
    __table_args__ = (
            db.PrimaryKeyConstraint('taxon_id', 'name', 'name_class'),
            {'extend_existing':True, 'autoload':True})

    def serialize(self):
        return {
            'taxon_id':self.taxon_id,
            'name':self.name,
            'name_class':self.name_class
        }

    def __str__(self):
        return f'{self.name} {self.name_class}'
