import sys, os
from psycopg2.errors import IntegrityError

def run(conn, filename, format, type, id):

    if type=='biodatabase':
        try:
            db = conn[id]
            from Bio import SeqIO
            SeqIO.write(db.values(), filename, format)
            return len(db), 0, format, f'Downloaded {len(db)} sequences from "{id}".'
        except IntegrityError as e:
            return 0, 0, 'unknown', f'The database "{biodb}" does not exist.'

    # db = conn[id]
    # for identifier in ['6273291', '6273290', '6273289'] :
    #     seq_record = db.lookup(gi=identifier)
    #     print seq_record.id, seq_record.description[:50] + "..."
    #     print "Sequence length %i," % len(seq_record.seq)
    #
    # db = conn["orchids"]
    # print "This database contains %i records" % len(db)
    # for key, record in db.iteritems():
    #     print "Key %r maps to a sequence record with id %s" % (key, record.id)
    #
    # n, total, format = upload_file(conn, filename, db)
    # return n, total, format, f'Number of sequencies saved: {n}/{total}'


def prepare_download(conn, type, id):
    print(f'>> File: {filepath}')

    formats = ['seqxml', 'embl', 'fasta', 'gb', 'gck', 'genbank']
    name, ext = os.path.splitext(filepath)
    if ext[1:] in formats:
        formats.insert(0, ext[1:])

    from Bio import SeqIO
    for format in formats:
        ffound = False
        try:
            seqs = list(SeqIO.parse(filepath, format))
        except Exception as e:
            print(f'FORMAT failed: {format}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            continue

        n = total = 0
        for seq in seqs:
            ffound = True
            try:
                total+=1
                n += db.load([seq],True)
                conn.commit()
            except IntegrityError as e:
                conn.rollback()
                continue

        if not ffound:
            print(f'FORMAT failed: {format}')
            continue

        conn.commit()
        return n, total, format


    return 0, 0, 'unknown'
