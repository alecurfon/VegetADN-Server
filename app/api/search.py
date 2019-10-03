# SELECT  *
# FROM    ( SELECT    ROW_NUMBER() OVER ( ORDER BY OrderDate ) AS RowNum, *
#           FROM      Orders
#           WHERE     OrderDate >= '1980-01-01'
#         ) AS RowConstrainedResult
# WHERE   RowNum >= 1
#     AND RowNum < 20
# ORDER BY RowNum

from flask_restful import Resource
from flask import abort, request

class Search(Resource):
    methods = ['GET']

    def get(self):
        print(f'\n### GET(search) request:\n{request}')

        print(request.args)
        if ('type' not in request.args) or ('search' not in request.args):
            abort(400, description=f'Params are missing.')
        if request.args['type'] not in ('biodatabase', 'bioentry', 'taxon'):
            abort(409, description=f'Search of type {type} is not available.')

        if request.args['type'] == 'biodatabase':
            return self.getBioDB(request.args['search'])
        if request.args['type'] == 'bioentry':
            return self.getBioentry(request.args['search'])
        if request.args['type'] == 'taxon':
            return self.getTaxon(request.args['search'])


    def getBioDB(self, concept):
        from ..models import Session, Base
        session = Session()
        from ..models.biodatabase import Biodatabase
        query = session.query(Biodatabase)
        query = query.filter(Biodatabase.name.ilike(f'%{concept}%'))
        result = []
        for b in query.all():
            result.append(b.serialize())
        print(f'Sending:\n{result}')
        session.close()
        return result, 200


    def getBioentry(self, concept):
        print(f'Looking for a bioentry like {concept}')
        return [f'Looking for a bioentry like {concept}']


    def getTaxon(self, concept):
        print(f'Looking for a taxon like {concept}')
        return [f'Looking for a taxon like {concept}']
