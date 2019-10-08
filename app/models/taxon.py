# coding=utf-8

from . import db

class Taxon(db.Model):
    __tablename__ = 'taxon'

    taxon_id = db.Column(db.Integer, primary_key=True)
    ncbi_taxon_id = db.Column(db.Integer)
    parent_taxon_id = db.Column(db.Integer)
    node_rank = db.Column(db.String(32))
    genetic_code = db.Column(db.Integer)
    mito_genetic_code = db.Column(db.Integer)
    left_value = db.Column(db.Integer)
    right_value = db.Column(db.Integer)

    # def __init__(self, taxon_id, ncbi_taxon_id, parent_taxon_id, node_rank,
    #     genetic_code, mito_genetic_code, left_value, right_value):
    #         self.taxon_id = taxon_id
    #         self.ncbi_taxon_id = ncbi_taxon_id
    #         self.parent_taxon_id = parent_taxon_id
    #         self.node_rank = node_rank
    #         self.genetic_code = genetic_code
    #         self.mito_genetic_code = mito_genetic_code
    #         self.left_value = left_value
    #         self.right_value = right_value

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
