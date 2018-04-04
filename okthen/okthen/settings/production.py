from okthen.settings.common import *
import dj_database_url

WSGI_APPLICATION = 'okthen.wsgi.application'
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
