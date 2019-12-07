from flask_restful import Resource
from flask import abort, request

class Biodatabase(Resource):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get(self, id=-1, name=None):
        print(f'\n### GET(biodatabase) request:\n{request}')

        from app.models import Biodatabase
        query = Biodatabase.query
        try:
            if id > -1:
                query = query.filter(Biodatabase.biodatabase_id == id)
            elif name!=None:
                query = query.filter(Biodatabase.name == name)
            else:
                query = query.order_by(Biodatabase.name)
        except Exception as e:
            abort(404, description='Biodatabase not found.')

        result = []
        n_seqs = -1
        count = ('count' in request.args) and (request.args['count']=='yes')
        if count:
            from app.models import Bioentry
        for row in query.all():
            if count:
                n_seqs = Bioentry.query.filter(Bioentry.biodatabase_id==row.biodatabase_id).count()
            b=row.serialize()
            b['count']=n_seqs
            result.append(b)
        return result, 200


    # with Biopython
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


    def put(self, id=None, id_name=None):
        print(f'\n### PUT(biodatabase) request:\n{request}')

        self.__data_check(request.json)
        from app import db
        from app.models import Biodatabase
        try:
            if id!=None:
                row = Biodatabase.query.filter(Biodatabase.biodatabase_id == id)
            elif id_name!=None:
                row = Biodatabase.query.filter(Biodatabase.name == id_name)
            else:
                abort(404, description='Biodatabase identifier is missing.')
        except Exception as e:
            abort(404, description='Biodatabase not found.')
        row.update({'name':self.name, 'authority':self.authority, 'description':self.description})
        db.session.commit()
        db.session.close()
        return {'message':f'Biodatabase "{self.name}" updated.'}, 201


    # with Biopython
    def delete(self, id=-1, id_name=None):
        print(f'\n### DELETE(biodatabase) request:\n{request}')

        data, code = self.get(id, id_name)
        if code == 404:
            abort(404, description='Biodatabase not found.')
        biodatabase = data[0]['name']
        from app.utils.biopy_db import connect
        conn = connect()
        n_seqs = len(conn[biodatabase])
        conn.remove_database(biodatabase)
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
