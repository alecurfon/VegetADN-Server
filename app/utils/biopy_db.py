def connect():
    from BioSQL import BioSeqDatabase
    return BioSeqDatabase.open_database(driver = "psycopg2", user = "administrador",
        host = "localhost", db = "biosql")
    # from Bio import Entrez
    # Entrez.email = 'alejandro.curbelo103@alu.ulpgc.es'
