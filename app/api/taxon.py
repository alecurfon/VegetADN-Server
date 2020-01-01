from flask_restful import Resource
from flask import abort, request
from app.auth import *

class Taxon(Resource):
    methods = ['GET']


    @token_required
    def get(self, id=-1, name=None):
        print(f'\n### GET(taxon) request:\n{request}')

        from app.models import TaxonName
        result = []
        query = TaxonName.query
        if id > -1:
            try:
                query = query.filter(TaxonName.taxon_id == id) \
                    .order_by(TaxonName.name_class)
            except Exception as e:
                abort(404, description='TaxonName not found.')
        elif name!=None:
            try:
                result = [query.filter(TaxonName.name == name).first().serialize()]
                query = query.filter(TaxonName.taxon_id == result[0]['taxon_id']) \
                    .filter(TaxonName.name != result[0]['name']) \
                    .order_by(TaxonName.name_class)
            except Exception as e:
                abort(404, description='TaxonName not found.')
        else:
            query = query.order_by(TaxonName.name)
        for b in query.all():
            result.append(b.serialize())
        return result, 200
