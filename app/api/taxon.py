from flask_restful import Resource
from flask import abort, request

class Taxon(Resource):
    methods = ['GET']


    def get(self, id=-1, name=None):
        print(f'\n### GET(taxon) request:\n{request}')

        from app.models import TaxonName
        query = TaxonName.query
        if id > -1:
            try:
                result = query.filter(TaxonName.taxon_id == id).first().serialize()
            except Exception as e:
                abort(404, description='TaxonName not found.')
        elif name!=None:
            try:
                result = query.filter(TaxonName.name == name).first().serialize()
            except Exception as e:
                abort(404, description='TaxonName not found.')
        else:
            query = query.order_by(TaxonName.name)
            result = []
            for b in query.all():
                result.append(b.serialize())
        return result, 200
