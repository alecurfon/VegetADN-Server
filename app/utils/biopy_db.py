def connect():
    from BioSQL import BioSeqDatabase
    return BioSeqDatabase.open_database(driver = "psycopg2", user = "administrador",
        host = "localhost", db = "vegetadn")
