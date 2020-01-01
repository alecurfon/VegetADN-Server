from app import db

class Biodatabase(db.Model):
    __tablename__ = 'biodatabase'
    __table_args__ = {'autoload':True}

    def serialize(self):
        return {
            'biodatabase_id': self.biodatabase_id,
            'name': self.name,
            'authority': self.authority,
            'description': self.description
        }

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
