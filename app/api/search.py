from flask_restful import Resource
from flask import abort, request

class Search(Resource):
    methods = ['GET']

    def get(self):
        print(f'\n### GET(search) request:\n{request}')

        print(request.args)
        if ('type' not in request.args) or ('search' not in request.args) \
            or ('page' not in request.args) or ('page_size' not in request.args):
            abort(400, description=f'Params are missing.')
        if request.args['type'] not in ('biodatabase', 'bioentry', 'taxon'):
            abort(409, description=f'Search of type {type} is not available.')
        if not (request.args['page'].isdigit() and request.args['page_size'].isdigit()):
            abort(409, description='The page information is incorrect.')

        print(f'>> SEARCH: {request.args["search"]}')
        if request.args['type'] == 'biodatabase':
            return self.getBioDB(request.args['search'],
                request.args['page'], request.args['page_size'])
        if request.args['type'] == 'bioentry':
            return self.getBioentry(request.args['search'],
                request.args['page'], request.args['page_size'])
        if request.args['type'] == 'taxon':
            return self.getTaxon(request.args['search'],
                request.args['page'], request.args['page_size'])


    def getBioDB(self, search, page, page_size):
        from ..models import db, Biodatabase
        query = db.session.query(Biodatabase) \
            .filter((Biodatabase.name.ilike(f'%{search}%'))
                | (Biodatabase.authority.ilike(f'%{search}%'))
                | (Biodatabase.description.ilike(f'%{search}%'))) \
            .paginate(int(page), int(page_size), False)
        result = []
        for b in query.items:
            result.append(b.serialize())
        db.session.close()
        return {'result': result, 'pages' : query.pages, 'total' : query.total}, 200


    def getBioentry(self, search, page, page_size):
        from ..models import db, Bioentry
        query = db.session.query(Bioentry) \
            .filter((Bioentry.name.ilike(f'%{search}%'))
                # | (Bioentry.accession.ilike(f'%{search}%'))
                # | (Bioentry.identifier.ilike(f'%{search}%'))
                | (Bioentry.division.ilike(f'%{search}%'))
                | (Bioentry.description.ilike(f'%{search}%'))) \
            .paginate(int(page), int(page_size), False)
        result = []
        for b in query.items:
            result.append(b.serialize())
        db.session.close()
        return {'result': result, 'pages' : query.pages, 'total' : query.total}, 200


    def getTaxon(self, search, page, page_size):
        from ..models import db, TaxonName
        query = db.session.query(TaxonName) \
            .filter((TaxonName.name.ilike(f'%{search}%'))
                | (TaxonName.name_class.ilike(f'%{search}%'))) \
            .paginate(int(page), int(page_size), False)
        result = []
        for b in query.items:
            result.append(b.serialize())
        db.session.close()
        return {'result': result, 'pages' : query.pages, 'total' : query.total}, 200
