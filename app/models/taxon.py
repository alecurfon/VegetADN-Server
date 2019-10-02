# coding=utf-8

from . import Base
from sqlalchemy import Column, String, Integer

class Taxon(Base):
    __tablename__ = 'taxon'

    taxon_id = Column(Integer, primary_key=True)
    ncbi_taxon_id = Column(Integer)
    parent_taxon_id = Column(Integer)
    node_rank = Column(String(32))
    genetic_code = Column(Integer(16))
    mito_genetic_code = Column(Integer(16))
    left_value = Column(Integer)
    right_value = Column(Integer)

    def __init__(self, taxon_id, ncbi_taxon_id, parent_taxon_id, node_rank,
        genetic_code, mito_genetic_code, left_value, right_value):
            self.taxon_id = taxon_id
            self.ncbi_taxon_id = ncbi_taxon_id
            self.parent_taxon_id = parent_taxon_id
            self.node_rank = node_rank
            self.genetic_code = genetic_code
            self.mito_genetic_code = mito_genetic_code
            self.left_value = left_value
            self.right_value = right_value

    def serialize(self):
        return {
            'taxon_id':taxon_id,
            'ncbi_taxon_id':ncbi_taxon_id,
            'parent_taxon_id':parent_taxon_id,
            'node_rank':node_rank,
            'genetic_code':genetic_code,
            'mito_genetic_code':mito_genetic_code,
            'left_value':left_value,
            'right_value':right_value
        }
