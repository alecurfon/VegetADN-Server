from flask_restful import Resource
from flask import abort, request

class Search(Resource):
    methods = ['GET']

    def get(self):
        print(f'\n### GET(search) request:\n{request}')
        self.check_args(request.args)

        query = self.get_query(request.args)

        result = []
        for b in query.items:
            result.append(b.serialize())
        response = {'result': result, 'pages' : query.pages, 'total' : query.total}

        return response, 200

    def check_args(self, args):
        print(args)
        if ('type' not in args) or ('search' not in args) \
            or ('page' not in args) or ('page_size' not in args):
            abort(400, description=f'Params are missing.')
        if args['type'] not in ('biodatabase', 'bioentry', 'taxon'):
            abort(409, description=f'Search of type {type} is not available.')
        if not (args['page'].isdigit() and args['page_size'].isdigit()):
            abort(409, description='The page information is incorrect.')

    def get_query(self, args):
        print(f'>> SEARCH: {args["search"]}')

        if args['type'] == 'biodatabase':
            from ..models import Biodatabase
            query = Biodatabase.query \
                .filter(Biodatabase.match(Biodatabase, args['search'])) \

        if args['type'] == 'bioentry':
            from ..models import Bioentry
            query = Bioentry.query \
                .filter(Bioentry.match(Bioentry, args['search'])) \

        if args['type'] == 'taxon':
            from ..models import TaxonName
            query = TaxonName.query \
                .filter(TaxonName.match(TaxonName, args['search']))

        print(query)
        return query.paginate(int(args['page']), int(args['page_size']), False)
