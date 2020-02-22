from flask_restful import Resource
from flask import abort, request
from app.auth import *

class Biodatabase(Resource):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    @token_required
    def get(self, name=None):
        print(f'\n### GET(biodatabase) request:\n{request}')

        count = ('count' in request.args) and (request.args['count']=='yes')

        from app.models import Biodatabase
        query = Biodatabase.query

        if name!=None:
            try:
                query = query.filter(Biodatabase.name == name).first()
                result = query.serialize()
            except Exception as e:
                abort(404, description='Biodatabase not found.')
            if count:
                n_seqs = self.getCount(query)
                result['count']=n_seqs
        else:
            query = query.order_by(Biodatabase.name)
            if ('bioentry' in request.args):
                from app.models import Bioentry
                query = query.join(Bioentry) \
                    .filter(Bioentry.accession == request.args['bioentry'])
            result = []
            for row in query.all():
                b = row.serialize()
                if count:
                    b['count'] = self.getCount(row)
                result.append(b)
        return result, 200


    def getCount(self, biodb):
        from app.models import Bioentry
        return Bioentry.query.filter(Bioentry.biodatabase_id==biodb.biodatabase_id).count()


    # with Biopython
    @admin_token_required
    def post(self):
        print(f'\n### POST(biodatabase) request:\n{request}')

        self.__data_check(request.json)
        from app.utils.biopy_db import connect
        conn = connect()
        try:
            db = conn[self.name]
            abort(409, description=f'The database "{self.name}" already exists.')
        except KeyError as e:
            db = conn.new_database(self.name, authority=self.authority, description=self.description)
            conn.commit()

        msg = { 'message':f'Biodatabase "{self.name}" created.' }
        conn.close()
        return msg, 201


    @admin_token_required
    def put(self, name=None):
        print(f'\n### PUT(biodatabase) request:\n{request}')

        self.__data_check(request.json)
        from app import db
        from app.models import Biodatabase
        try:
            if name!=None:
                row = Biodatabase.query.filter(Biodatabase.name == name)
            else:
                abort(404, description='Biodatabase identifier is missing.')
        except Exception as e:
            abort(404, description='Biodatabase not found.')
        row.update({'name':self.name, 'authority':self.authority, 'description':self.description})
        db.session.commit()
        db.session.close()
        return {'message':f'Biodatabase "{self.name}" updated.'}, 201


    # with Biopython
    @admin_token_required
    def delete(self, name=None):
        print(f'\n### DELETE(biodatabase) request:\n{request}')

        data, code = self.get(name)
        if code == 404:
            abort(404, description='Biodatabase not found.')
        biodatabase = data['name']
        from app.utils.biopy_db import connect
        conn = connect()
        n_seqs = len(conn[biodatabase])
        # conn.remove_database(biodatabase)
        del conn[biodatabase]
        conn.commit()
        conn.close()
        return {'message':f'Biodatabase "{biodatabase}" removed with its {n_seqs} sequences.'}, 201


    def __data_check(self, data):
        print(f'>>> CHECKING {data}')

        if 'name' not in data:
            abort(400, description=f'Data is missing for {data}')
        self.name = data['name']
        if data['name'] == None:
            self.name = ''
        self.authority = ''
        if 'authority' in data:
            self.authority = data['authority']
        self.description = ''
        if 'description' in data:
            self.description = data['description']
