
def connect():
    from config import DBDRIVER, DBUSER, DBPASSWD, DBHOST, DBNAME
    from Bio import Entrez
    Entrez.email = f'{DBUSER}@{DBNAME}.com'
    from BioSQL import BioSeqDatabase
    return BioSeqDatabase.open_database(driver = DBDRIVER, user = DBUSER,
        passwd = DBPASSWD, host = DBHOST, db = DBNAME)
