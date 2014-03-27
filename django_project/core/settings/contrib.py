from .base import *

# Extra installed apps
INSTALLED_APPS += (
    # 'raven.contrib.django',  # enable Raven plugin
    'south',
    'pipeline',
    'social.apps.django_app.default',
)

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# python social auth required settings
AUTHENTICATION_BACKENDS = (
    'social.backends.openstreetmap.OpenStreetMapOAuth',
)

SOCIAL_AUTH_OPENSTREETMAP_KEY = 'xuq0sXds8n9Bi2E6wcs49Y9vLREYVixxQkjcU2TF'
SOCIAL_AUTH_OPENSTREETMAP_SECRET = 'Hjpv6n9jm7ejSuB0N5TvPAznq5k69vAD9vzdyLzH'
