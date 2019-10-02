from flask_restful import Resource
from flask import abort, request

class BiodbAPI(Resource):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get(self, id=-1):
        print(f'\n### GET(biodatabase) request:\n{request}')

        from ..models import Session, Base
        session = Session()
        from ..models.biodatabase import Biodatabase
        if id==-1:
            query = session.query(Biodatabase)
            query = query.order_by(Biodatabase.name)
            # query = query.order_by(Biodatabase.authority)
            result = []
            for b in query.all():
                result.append(b.serialize())
            print(f'Sending:\n{result}')
        else:
            try:
                result = session.query(Biodatabase).filter(Biodatabase.biodatabase_id == id).first()
            except Exception as e:
                session.close()
                abort(404, description='Biodatabase not found.')
        session.close()
        return result, 200


    def post(self):
        print(f'\n### POST(biodatabase) request:\n{request}')

        name, authority, description = self.__data_check(request.json)
        from ..tools.db_link import connect
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
        from ..models import Session, Base
        session = Session()
        from ..models.biodatabase import Biodatabase
        try:
            row = session.query(Biodatabase).filter(Biodatabase.biodatabase_id == id).first()
        except Exception as e:
            session.rollback()
            session.close()
            abort(404, description='Biodatabase not found.')
        row.name = name
        row.authority = authority
        row.description = description
        session.commit()
        session.close()
        return {'message':f'Biodatabase "{name}" updated.'}, 201

    def delete(self, id):
        print(f'\n### DELETE(biodatabase) request:\n{request}')

        data, code = self.get(id)
        if code == 404:
            abort(404, description='Biodatabase not found.')

        from ..tools.db_link import connect
        conn = connect()
        conn.remove_database(data.name)
        conn.commit()
        conn.close()
        return {'message':f'Biodatabase "{data.name}" removed.'}, 201


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
