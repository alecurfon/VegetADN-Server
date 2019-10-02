
def run(entry_id):
    print(' - Query:',
            'SELECT be.* ',
            'FROM bioentry be INNER JOIN biodatabase bd',
            'ON bd.biodatabase_id = be.biodatabase_id',
            'WHERE bd.name = %s AND be.accession = %s;')

    try:
        from load_genbank_file import *
        server = connect()
        db = server['biosql']
        record = db.lookup(accession = entry_id)

        print(f'\n - Record:\n ID: {record.id}\n Name: {record.name}\n Description: {record.description}')

        sequence = record.seq
        print(f'\n - Sequence:\n Alphabet: {sequence.alphabet}\n First five nucleotides: {sequence[:5].tostring()}')

        feature = record.features[0]
        print(f'\n - Features:\n Type: {feature.type}\n Location: {feature.location}\n Qualifiers: {feature.qualifiers}')
    except:
        print('An exception occurred.')

if __name__=='__main__':
    run('Z78532')
