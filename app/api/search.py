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

    def get(self, type):
        print(f'\n### GET(search) request:\n{request}')

        if type == 'biodatabase':
            return self.getBioDB(request.form['search'])
        if type == 'bioentry':
            return self.getBioentry(request.form['search'])
        if type == 'taxon':
            return self.getTaxon(request.form['search'])

        # from ..models import Session, Base
        # session = Session()
        # from ..models.biodatabase import Biodatabase
        # if id==-1:
        #     query = session.query(Biodatabase)
        #     query = query.order_by(Biodatabase.name)
        #     # query = query.order_by(Biodatabase.authority)
        #     result = []
        #     for b in query.all():
        #         result.append(b.serialize())
        #     print(f'Sending:\n{result}')
        # else:
        #     try:
        #         result = session.query(Biodatabase).filter(Biodatabase.biodatabase_id == id).first()
        #     except Exception as e:
        #         session.close()
        #         abort(404, description='Biodatabase not found.')
        # session.close()
        # return result, 200


    def getBioDB(self, concept):
        print(f'Looking for biodb a like {concept}')
        return f'Looking for biodb a like {concept}'


    def getBioentry(self, concept):
        print(f'Looking for bioentry a like {concept}')
        return f'Looking for bioentry a like {concept}'


    def getTaxon(self, concept):
        print(f'Looking for taxon a like {concept}')
        return f'Looking for taxon a like {concept}'
