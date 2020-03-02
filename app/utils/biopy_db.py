def connect():
    from BioSQL import BioSeqDatabase
    from config import PASSWORD
    return BioSeqDatabase.open_database(driver = "psycopg2", user = "vegetadn",
        passwd = PASSWORD, host = "localhost", db = "vegetadn")
