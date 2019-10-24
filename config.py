import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TESTING = False
SQLALCHEMY_DATABASE_URI = 'postgresql://administrador:@localhost:5432/biosql'
# SQLALCHEMY_ENGINE_OPTIONS = {
#     'pool': QueuePool(),
#     'pool_size' : 10,
#     'pool_recycle':120,
#     'pool_pre_ping': True
# }
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}


# ADMINS = frozenset(['youremail@yourdomain.com'])
# SECRET_KEY = 'SecretKeyForSessionSigning'

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')

# THREADS_PER_PAGE = 8

# CSRF_ENABLED = True
# CSRF_SESSION_KEY = "somethingimpossibletoguess"

# RECAPTCHA_USE_SSL = False
# RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
# RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
# RECAPTCHA_OPTIONS = {'theme': 'white'}
