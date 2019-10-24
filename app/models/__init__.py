from .biodatabase import Biodatabase
from .bioentry import Bioentry
from .biosequence import Biosequence
from .taxon_name import TaxonName
from .taxon import Taxon

def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector('english', exp)
