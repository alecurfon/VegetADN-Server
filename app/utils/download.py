from psycopg2.errors import IntegrityError

def run(conn, filename, format, biodatabase, bioentry):
    nseqs = 0
    try:
        db = conn[biodatabase]
        if bioentry=='':
            data = db.values()
            nseqs = len(db)
        else:
            data = db.lookup(accession=bioentry)
            nseqs = 1
    except IntegrityError as e:
        return f'The database "{biodb}" or the bioentry "{bioentry}" does not exist.'

    from Bio import SeqIO
    SeqIO.write(data, open(filename, "w"), format)
    return f'Downloaded {nseqs} sequences from "{biodatabase}".'
