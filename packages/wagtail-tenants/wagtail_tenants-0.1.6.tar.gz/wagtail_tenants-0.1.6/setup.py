# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtail_tenants',
 'wagtail_tenants.customers',
 'wagtail_tenants.customers.migrations',
 'wagtail_tenants.db',
 'wagtail_tenants.management',
 'wagtail_tenants.management.commands',
 'wagtail_tenants.middleware',
 'wagtail_tenants.migrations',
 'wagtail_tenants.users',
 'wagtail_tenants.users.migrations',
 'wagtail_tenants.users.views']

package_data = \
{'': ['*'],
 'wagtail_tenants': ['templates/wagtail_tenants/admin/*',
                     'templates/wagtailadmin/home/*',
                     'templates/wagtailusers/users/*']}

install_requires = \
['django-dbbackup>=3.3.0,<4.0.0',
 'django-tenants>=3.3.4,<4.0.0',
 'myst-parser>=0.15.2,<0.16.0',
 'psycopg2>=2.9.2,<3.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'wagtail-tenants',
    'version': '0.1.6',
    'description': 'Adds multitenancy based on django_tenants to wagtail cms',
    'long_description': '# wagtail-tenants\n\n[![Documentation Status](https://readthedocs.org/projects/wagtail-tenants/badge/?version=latest)](https://wagtail-tenants.readthedocs.io/en/latest/?badge=latest)\n[![Testing the wagtail tenants with postgres](https://github.com/borisbrue/wagtail-tenants/actions/workflows/integrationtest.yml/badge.svg)](https://github.com/borisbrue/wagtail-tenants/actions/workflows/integrationtest.yml)\n\nwagtail_tenants is a Django/Wagtail app to provide multitenancy to your wagtail project.\nYou are able to run a main Wagtail Site and from within you are able to host as many Wagtailsites as you want. \ndjango_tenants is used to slice the database layer in a postgres database based on a given schema.\n\nDetailed documentation will be in the "docs" directory. \n\n## Quick start\n\n### Installation\n\n```bash\npip install wagtail-tenants\n```\n\n### Configuration\n\n1. Add "wagtail_tenants" to your INSTALLED_APPS setting like this:\n\n    ```python\n    SHARED_APPS = (\n        \'wagtail_tenants.customers\'\n        \'wagtail_tenants\',\n        \'wagtail.contrib.forms\',\n        ...\n        "wagtail_tenants.users",\n        "wagtail.users",\n        ...\n    )\n\n    TENANT_APPS = (\n        \'wagtail_tenants\',\n        "django.contrib.contenttypes",\n        ...\n        # rest of the wagtail apps\n        ...\n        "wagtail_tenants.users",\n        "wagtail.users",\n        ...\n    )\n\n    INSTALLED_APPS = list(SHARED_APPS) + [\n        app for app in TENANT_APPS if app not in SHARED_APPS\n    ]\n    ```\n\n2. Include the the tenants middleware at the beginning of your middlewares:\n\n    ```python\n    MIDDLEWARE = [\n    "wagtail_tenants.middleware.main.WagtailTenantMainMiddleware",\n    ...\n    ]\n    ```\n\n3. Define the Tenant model Constants (and also set the default auto field if not already done):\n\n    ```python\n    AUTH_USER_MODEL = \'wagtail_tenants.User\' \n    TENANT_MODEL = "customers.Client" \n    TENANT_DOMAIN_MODEL = "customers.Domain"\n    DEFAULT_AUTO_FIELD=\'django.db.models.AutoField\'\n    ```\n\n4. Set the Database backend to the **django_tenants** backend:\n\n    ```python\n    DATABASES = {\n        "default": {\n            "ENGINE": "django_tenants.postgresql_backend",\n            "NAME": "db_name",\n            "USER": "db_user",\n            "PASSWORD": "",\n            "HOST": "127.0.0.1",\n            "PORT": "5432",\n        }\n    }\n    ```\n\n5. Set the Database Router to work with the tenants:\n\n    ```python\n    DATABASE_ROUTERS = ("wagtail_tenants.routers.WagtailTenantSyncRouter",)\n    ```\n\n6. Set the authentication backend to fit to our Tenant model.\n\n    ```python\n    AUTHENTICATION_BACKENDS = [\n        \'wagtail_tenants.backends.TenantBackend\',\n    ]\n    ```\n\n7. Run the migrations with `./manage.py migrate_schemas --shared`\n8. Create a public schema with `./manage.py create_tenant`\n9. Create a superuser for the public tenant `./manage.py create_tenant_superuser`\n10. Start the Server and have fun\n11. You are able to create tenants within the admin of your public wagtailsite. If you want to log into a tenant you need at least one superuser for the tenant. You can use `./manage.py create_tenant_superuser` for that.\n',
    'author': 'Boris Brue',
    'author_email': 'boris@zuckersalzundpfeffer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://wagtail-tenants.readthedocs.io/en/latest/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
