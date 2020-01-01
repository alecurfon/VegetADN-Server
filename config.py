import os
_basedir = os.path.abspath(os.path.dirname(__file__))

from Bio import Entrez
Entrez.email = 'vegetADN@vegetadn.es'

DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'postgresql://administrador:@localhost:5432/vegetadn'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
SECRET_KEY = '\xfc\xfe\xad\xe1u\xd3=\xfd?\x00\xb6\xfeQ\x176\x17C\xd6\xfa\xf2\xfbK\x1f\xa0\xd6lx~\xcev.\xb4'
