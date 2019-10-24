import sys, os
from psycopg2.errors import IntegrityError


def run(conn, filepath, biodb):

    if not os.path.isfile(filepath):
        return 0, 0, 'unknown', f'{filepath} is not a file.'

    if os.path.getsize(filepath) == 0:
        return 0, 0, 'unknown', f'{filepath} is empty.'

    try:
        db = conn[biodb]
    except IntegrityError as e:
        return 0, 0, 'unknown', f'The database "{biodb}" does not exist.'

    n, total, format = upload_file(conn, filepath, db)
    return n, total, format, f'Number of sequencies saved: {n}/{total}'


# ['abi', 'abi-trim', 'ace', 'cif-atom', 'cif-seqres', 'clustal', 'embl', 'fasta', 'fasta-2line', 'fastq', 'fastq-sanger', 'fastq-solexa', 'fastq-illumina', 'gb', 'gck', 'genbank', 'ig', 'imgt', 'nexus', 'nib', 'pdb-seqres', 'pdb-atom', 'phd', 'phylip', 'pir', 'seqxml', 'sff', 'sff-trim', 'snapgene', 'stockholm', 'swiss', 'tab', 'qual', 'uniprot-xml', 'xdna']
# ['genbank', 'gb', 'fasta', 'embl', 'seqxml']
def upload_file(conn, filepath, db):
    print(f'>> File: {filepath}')

    formats = ['seqxml', 'embl', 'fasta', 'gb', 'gck', 'genbank', 'abi', 'abi-trim', 'ace', 'cif-atom', 'cif-seqres', 'clustal', 'fasta-2line', 'fastq', 'fastq-sanger', 'fastq-solexa', 'fastq-illumina', 'ig', 'imgt', 'nexus', 'nib', 'pdb-seqres', 'pdb-atom', 'phd', 'phylip', 'pir', 'sff', 'sff-trim', 'snapgene', 'stockholm', 'swiss', 'tab', 'qual', 'uniprot-xml', 'xdna']
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
