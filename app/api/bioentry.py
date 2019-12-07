from flask_restful import Resource
from flask import abort, request

class Bioentry(Resource):
    methods = ['GET']


    def get(self, id=-1, accession=None):
        print(f'\n### GET(bioentry) request:\n{request}')

        from app.models import Bioentry
        query = Bioentry.query
        if id > -1:
            try:
                result = query.filter(Bioentry.bioentry_id == id).first().serialize()
            except Exception as e:
                abort(404, description='Bioentry not found.')
        elif accession!=None:
            try:
                result = query.filter(Bioentry.accession == accession).first().serialize()
            except Exception as e:
                abort(404, description='Bioentry not found.')
        else:
            query = query.order_by(Bioentry.accession)
            result = []
            for b in query.all():
                result.append(b.serialize())
        return result, 200
