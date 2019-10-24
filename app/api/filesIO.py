import os
from flask_restful import Resource
from flask import abort, request
from werkzeug.utils import secure_filename

TMP_FOLDER = '/tmp'

class FilesIO(Resource):
    methods = ['POST']

    def post(self, biodb):
        print(f'\n### POST(filesIO) request:\n{request}')

        if len(request.files) < 1:
            abort(400, description='File list is missing.')

        from ..tools.db_link import connect
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
