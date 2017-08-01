"""
WSGI config for SalesForce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys


##########################################################################
#sys.path.append('/home/matt/Desktop/MPTCRM/SalesForce')
#sys.path.append('/home/matt/Desktop/MPTCRM/SalesForce/lib/site-packages')
##########################################################################

from django.core.wsgi import get_wsgi_application
#os.environ['HTTPS'] = "on"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SalesForce.settings")
#os.environ['wsgi.url_scheme'] = 'https'
application = get_wsgi_application()



