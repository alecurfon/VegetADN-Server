from flask_restful import Resource
from flask import abort, request

class Search(Resource):
    methods = ['GET']

    def get(self):
        print(f'\n### GET(search) request:\n{request}')
        self.__check_args(request.args)
        search = self.__get_paged_search(request.args)
        result = []
        for b in search.items:
            result.append(b.serialize())
        response = {'result': result, 'pages' : search.pages, 'total' : search.total}
        return response, 200


    def __check_args(self, args):
        print(args)
        if ('type' not in args) or ('search' not in args) \
            or ('page' not in args) or ('page_size' not in args):
            abort(400, description=f'Params are missing.')
        if args['type'] not in ('biodatabase', 'bioentry', 'taxon'):
            abort(409, description=f'Search of type {type} is not available.')
        if not (args['page'].isdigit() and args['page_size'].isdigit()):
            abort(409, description='The page information is incorrect.')


    def __get_paged_search(self, args):
        print(self.__get_query(args['type'], args['search']))
        return self.__get_query(args['type'], args['search']).paginate(int(args['page']), int(args['page_size']), False)


    def __get_query(self, type, search):
        search = ' & '.join(search.strip().split())
        if search=='':
            return self.__get_all(type)
        if type=='biodatabase':
            return self.__search_biodatabase(search)
        if type=='bioentry':
            return self.__search_bioentry(search)
        if type=='taxon':
            return self.__search_taxon(search)
        return query


    def __get_all(self, type):
        if type == 'biodatabase':
            from app.models import Biodatabase as Bioelement
        if type == 'bioentry':
            from app.models import Bioentry as Bioelement
        if type == 'taxon':
            from app.models import TaxonName as Bioelement
        return Bioelement.query


    def __search_biodatabase(self, terms):
        from app import db
        from app.models import Biodatabase
        return Biodatabase.query.filter(db.func.to_tsvector(
                Biodatabase.name
                + ' ' + db.func.coalesce(Biodatabase.authority, "")
                + ' ' + db.func.coalesce(Biodatabase.description, "")
            ).match(terms))


    def __search_bioentry(self, terms):
        from app import db
        from app.models import Biodatabase, Bioentry, TaxonName
        # .outerjoin(TaxonName, TaxonName.taxon_id == Bioentry.taxon_id) \
        return Bioentry.query \
            .join(Biodatabase) \
            .filter(db.func.to_tsvector(
                Bioentry.name
                + ' ' + Bioentry.accession
                + ' ' + db.func.coalesce(Bioentry.identifier, '')
                + ' ' + db.func.coalesce(Bioentry.division, '')
                + ' ' + db.func.coalesce(Bioentry.description , '')
                + ' ' + str(Bioentry.version)
                + ' ' + Biodatabase.name
                + ' ' + db.func.coalesce(Biodatabase.authority, "")
                + ' ' + db.func.coalesce(Biodatabase.description, "")
                # + ' ' + TaxonName.name + ' ' + TaxonName.name_class
            ).match(terms))


    def __search_taxon(self, terms):
        from app import db
        from app.models import TaxonName
        return TaxonName.query.filter(db.func.to_tsvector(
                TaxonName.name + ' ' + TaxonName.name_class
            ).match(terms))
