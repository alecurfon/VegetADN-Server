from flask_restful import Resource
from flask import abort, request

class BiodbAPI(Resource):
    methods = ['GET', 'POST', 'PUT', 'DELETE']


    def get(self, id=-1):
        print(f'\n### GET(biodatabase) request:\n{request}')

        from app.models import Biodatabase
        query = Biodatabase.query
        if id==-1:
            query = query.order_by(Biodatabase.name)
            # query = query.order_by(Biodatabase.authority)
            result = []
            for b in query.all():
                result.append(b.serialize())
        else:
            try:
                result = query.filter(Biodatabase.biodatabase_id == id).first()
            except Exception as e:
                abort(404, description='Biodatabase not found.')
        return result, 200


    # with Biopython
    def post(self):
        print(f'\n### POST(biodatabase) request:\n{request}')

        name, authority, description = self.__data_check(request.json)
        from app.utils.biopy_db import connect
        conn = connect()
        try:
            db = conn[name]
            abort(409, description=f'The database "{name}" already exists.')
        except KeyError as e:
            db = conn.new_database(name, authority=authority, description=description)
            conn.commit()

        msg = { 'name':name, 'authority':authority, 'description':description,
            'message':f'Biodatabase "{name}" created.' }
        conn.close()
        return msg, 201


    def put(self, id):
        print(f'\n### PUT(biodatabase) request:\n{request}')

        name, authority, description = self.__data_check(request.json)
        from app import db
        from app.models import Biodatabase
        try:
            row = Biodatabase.query.filter(Biodatabase.biodatabase_id == id)
        except Exception as e:
            abort(404, description='Biodatabase not found.')
        row.update({'name':name, 'authority':authority, 'description':description})
        db.session.commit()
        db.session.close()
        return {'message':f'Biodatabase "{name}" updated.'}, 201


    # with Biopython
    def delete(self, id):
        print(f'\n### DELETE(biodatabase) request:\n{request}')

        data, code = self.get(id)
        if code == 404:
            abort(404, description='Biodatabase not found.')

        from app.utils.biopy_db import connect
        conn = connect()
        n_seqs = len(conn[data.name])
        conn.remove_database(data.name)
        conn.commit()
        conn.close()
        return {'message':f'Biodatabase "{data.name}" removed with its {n_seqs} sequences.'}, 201


    def __data_check(self, data):
        print(f'>>> CHECKING {data}')

        if 'name' not in data:
            abort(400, description=f'Data is missing for {data}')
        name = data['name']
        if data['name'] == None:
            name = ''
        authority = ''
        if 'authority' in data:
            authority = data['authority']
        description = ''
        if 'description' in data:
            description = data['description']
        return name, authority, description
