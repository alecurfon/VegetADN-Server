from app import db

class Taxon(db.Model):
    __tablename__ = 'taxon'
    __table_args__ = {'autoload':True}

    def serialize(self):
        return {
            'taxon_id':self.taxon_id,
            'ncbi_taxon_id':self.ncbi_taxon_id,
            'parent_taxon_id':self.parent_taxon_id,
            'node_rank':self.node_rank,
            'genetic_code':self.genetic_code,
            'mito_genetic_code':self.mito_genetic_code,
            'left_value':self.left_value,
            'right_value':self.right_value
        }

    def __str__(self):
        return f'{self.node_rank} {self.genetic_code} {self.mito_genetic_code} {self.left_value} {self.right_value}'
