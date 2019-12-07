import os
from flask_restful import Resource
from flask import abort, request, send_file
from werkzeug.utils import secure_filename

TMP_FOLDER = '/tmp'

class FilesIO(Resource):
    methods = ['GET', 'POST']

    def get(self):
        print(f'\n### GET(filesIO) request:\n{request}')
        # filename, format, type[ biodatabase, bioentry, taxon ], id
        self.__check_args()
        filename = os.path.join(TMP_FOLDER, secure_filename(request.args['filename']))

        from app.utils.biopy_db import connect
        conn = connect()
        from ..utils import download
        nseq, ntotal, format, desc = download.run(conn, filename,
            request.args['format'], request.args['type'], request.args['id'])
        conn.close()

        return send_file(filename, mimetype='text/plain')

    def __check_args(self):
        print(request.args)
        if ('type' not in request.args) or ('id' not in request.args):
            abort(400, description=f'Params are missing.')
        if request.args['type'] not in ('biodatabase', 'bioentry', 'taxon'):
            abort(409, description=f'Download of type "{type}" is not available.')
        if ('format' not in request.args):
            request.args['format']='fasta'
        if request.args['format'] not in ('seqxml', 'embl', 'fasta', 'gb', 'gck', 'genbank'):
            abort(409, description=f'The download format "{type}" is not available.')
        if ('filename' not in request.args) or (request.args['filename'] == ''):
            request.args['filename']=f"{request.args['type']}_{request.args['id']}.{request.args['format']}"


    def post(self, biodb):
        print(f'\n### POST(filesIO) request:\n{request}')
        if len(request.files) < 1:
            abort(400, description='File list is missing.')

        from app.utils.biopy_db import connect
        conn = connect()

        msg = []
        for key,file in request.files.items(multi=True):

            if file.filename == '':
                msg.append({ 'status' : 409, 'msg': 'File "" unknown. Not selected file.' })
                continue

            file_cpy = os.path.join(TMP_FOLDER, secure_filename(file.filename))
            file.save(file_cpy)

            from ..utils import upload
            nseq, ntotal, format, desc = upload.run(conn, file_cpy, biodb)
            msg.append({ 'file' : file.filename, 'format' : format, 'upload_seqs' : nseq, 'total_seqs': ntotal , 'message': desc})

        conn.close()
        response = ''
        for i in msg:
            response += f"{i['file']}: {i['message']}\n"
            print(i)
        return response, 201
