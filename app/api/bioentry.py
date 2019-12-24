from flask_restful import Resource
from flask import abort, request

class Bioentry(Resource):
    methods = ['GET']

    def get(self, id=-1, accession=None):
        print(f'\n### GET(bioentry) request:\n{request}')

        self.__check_page()

        from app.models import Bioentry
        query = Bioentry.query
        if (id > -1) or (accession!=None):
            try:
                query = query.filter((Bioentry.bioentry_id == id) | (Bioentry.accession == accession))
                if 'biodatabase' in request.args:
                    return self.__attach(self.__biodatabase_filter(query, request.args['biodatabase']).first()), 200
            except Exception as e:
                abort(404, description='Bioentry not found.')
        else:
            query = query.order_by(Bioentry.accession)

        if 'biodatabase' in request.args:
            query = self.__biodatabase_filter(query, request.args['biodatabase'])

        if self.paged:
            return self.__get_paged(query), 200

        result = []
        for b in query.all():
            result.append(self.__attach(b))
        return result, 200


    def __check_page(self):
        if ('page' not in request.args) or ('page_size' not in request.args):
            self.paged = False
            return
        if not (request.args['page'].isdigit() and request.args['page_size'].isdigit()):
            abort(409, description='The page information is incorrect.')
        self.paged = True
        self.page = request.args['page']
        self.page_size = request.args['page_size']


    def __biodatabase_filter(self, query, biodb):
        from app.models import Biodatabase
        return query.join(Biodatabase) \
            .filter(Biodatabase.name == biodb)


    def __get_paged(self, query):
        query = query.paginate(int(self.page), int(self.page_size), False)
        result = []
        for b in query.items:
            result.append(self.__attach(b))
        return {'result': result, 'pages' : query.pages, 'total' : query.total}


    def __attach(self, bioentry):
        result=bioentry.serialize()
        from app.models import Biodatabase
        result['biodatabase'] = Biodatabase.query \
            .filter(Biodatabase.biodatabase_id==bioentry.biodatabase_id) \
            .first().serialize()
        from app.models import TaxonName
        try:
            result['taxon'] = TaxonName.query \
                .filter(TaxonName.taxon_id==bioentry.taxon_id) \
                .filter(TaxonName.name_class=='scientific name') \
                .first().serialize()
        except Exception as e:
            result['taxon'] = None
        if ('sequence' in request.args) and (request.args['sequence']=='yes'):
            from app.utils import connect
            biodb_conn = connect()[result['biodatabase']['name']]
            sequence = biodb_conn.lookup(accession=result['accession'])
            result['sequence'] = sequence.format('gb')
        return result
