Simple JWT
==========

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband
.. image:: https://github.com/jazzband/djangorestframework-simplejwt/workflows/Test/badge.svg
   :target: https://github.com/jazzband/djangorestframework-simplejwt/actions
   :alt: GitHub Actions
.. image:: https://codecov.io/gh/jazzband/djangorestframework-simplejwt/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/jazzband/djangorestframework-simplejwt
.. image:: https://img.shields.io/pypi/v/djangorestframework-simplejwt.svg
  :target: https://pypi.python.org/pypi/djangorestframework-simplejwt
.. image:: https://img.shields.io/pypi/pyversions/djangorestframework-simplejwt.svg
  :target: https://pypi.python.org/pypi/djangorestframework-simplejwt
.. image:: https://img.shields.io/pypi/djversions/djangorestframework-simplejwt.svg
  :target: https://pypi.python.org/pypi/djangorestframework-simplejwt
.. image:: https://readthedocs.org/projects/django-rest-framework-simplejwt/badge/?version=latest
  :target: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

Abstract
--------

Simple JWT is a JSON Web Token authentication plugin for the `Django REST
Framework <http://www.django-rest-framework.org/>`__.

For full documentation, visit `django-rest-framework-simplejwt.readthedocs.io
<https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>`__.


Description
--------
This package is a fork of `django-rest-framework-simplejwt.readthedocs.io
<https://django-rest-framework-simplejwt.readthedocs.io/en/latest/>`__. To prevent conflict in package name I rename the package name to `djangorestframework-passwordless-simplejwt`.
So all the configuration for the base package can be use. You need only use new name as `app_name`.
In this extension I add passwordless mecanism based on calling an API.
In the provided aendpoint developer have to define how he/she want to handle passwordless.

You onle need add this line to your settings.py file in base project.


`OTP_CONFIGS ={
    'base_url': "https://example.com/api/send.json",
    'receptor_key': "receptor",
    'message_key': "message",
}`

`receptor_key` is the value of receptor key in endpoint side.
