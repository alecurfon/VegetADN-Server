import os
from flask_restful import Resource
from flask import request, abort as end_request, send_file
from werkzeug.utils import secure_filename

from ..auth import *

TMP_FOLDER = '/tmp'

class FilesIO(Resource):
    methods = ['GET', 'POST']

    @token_required
    def get(self):
        print(f'\n### GET(filesIO) request:\n{request}')
        self.__check_get_args()
        self.filename = os.path.join(TMP_FOLDER, secure_filename(self.filename))

        from ..utils.biopy_db import connect
        conn = connect()
        from ..utils import download
        desc = download.run(conn, self.filename, self.format,
            self.biodatabase, self.bioentry)
        conn.close()
        print(desc)
        return send_file(self.filename, mimetype='text/plain')

    def __check_get_args(self):
        print(request.args)
        if ('biodatabase' not in request.args):
            end_request(400, description=f'The biodatabase is not specified.')
        self.biodatabase = request.args['biodatabase']
        if ('bioentry' not in request.args):
            self.bioentry = ''
        else:
            self.bioentry = request.args['bioentry']
        if ('format' not in request.args):
            self.format = 'fasta'
        else:
            self.format = request.args['format']
        if self.format not in ('embl', 'fasta', 'gb', 'genbank'):
            end_request(400, description=f'The format {self.format} is not available.')
        if ('filename' not in request.args) or (request.args['filename'] == ''):
            self.filename = f"{request.args['biodatabase']}_download.{request.args['format']}"
        else:
            self.filename = request.args['filename']


    @admin_token_required
    def post(self, biodb):
        print(f'\n### POST(filesIO) request:\n{request}')
        if len(request.files) < 1:
            end_request(400, description='File list is missing.')

        from ..utils.biopy_db import connect
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
