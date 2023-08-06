# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_helpers']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.0', 'alembic>=1.6.5']

extras_require = \
{'docs': ['sphinx>=4,<5', 'myst-parser>=0.16.1,<0.17.0'],
 'flask': ['Flask>=2.0,<3.0']}

setup_kwargs = {
    'name': 'sqlalchemy-helpers',
    'version': '0.9.0',
    'description': 'SQLAlchemy Helpers',
    'long_description': '# SQLAlchemy Helpers\n\nThis project contains a tools to use SQLAlchemy and Alembic in a project.\n\nIt has a Flask integration, and other framework integrations could be added in\nthe future.\n\nThe full documentation is [on ReadTheDocs](https://sqlalchemy-helpers.readthedocs.io>).\n\nYou can install it [from PyPI](https://pypi.org/project/sqlalchemy-helpers/).\n\n![PyPI](https://img.shields.io/pypi/v/sqlalchemy-helpers.svg)\n![Supported Python versions](https://img.shields.io/pypi/pyversions/sqlalchemy-helpers.svg)\n![Tests status](https://github.com/fedora-infra/sqlalchemy-helpers/actions/workflows/tests.yml/badge.svg?branch=develop)\n![Documentation](https://readthedocs.org/projects/sqlalchemy-helpers/badge/?version=latest)\n\n## Flask integration\n\nThis is how you can use the Flask integration.\n\nFirst, create a python module to instanciate the `DatabaseExtension`, and\nre-export some useful helpers:\n\n```python\n# database.py\n\nfrom sqlalchemy_helpers import Base, get_or_create, is_sqlite, exists_in_db\nfrom sqlalchemy_helpers.flask_ext import DatabaseExtension, get_or_404, first_or_404\n\ndb = DatabaseExtension()\n```\n\nIn the application factory, import the instance and call its `.init_app()` method:\n\n```python\n# app.py\n\nfrom flask import Flask\nfrom sqlalchemy_helpers.database import db\n\ndef create_app():\n    """See https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/"""\n\n    app = Flask(__name__)\n\n    # Load the optional configuration file\n    if "FLASK_CONFIG" in os.environ:\n        app.config.from_envvar("FLASK_CONFIG")\n\n    # Database\n    db.init_app(app)\n\n    return app\n```\n\nYou can declare your models as you usually would with SQLAlchemy, just inherit\nfrom the `Base` class that you re-exported in `database.py`:\n\n```python\n# models.py\n\nfrom sqlalchemy import Column, Integer, Unicode\n\nfrom .database import Base\n\n\nclass User(Base):\n\n    __tablename__ = "users"\n\n    id = Column("id", Integer, primary_key=True)\n    name = Column(Unicode(254), index=True, unique=True, nullable=False)\n    full_name = Column(Unicode(254), nullable=False)\n    timezone = Column(Unicode(127), nullable=True)\n```\n\nIn your views, you can use the instance\'s `session` property to access the\nSQLAlchemy session object. There are also functions to ease classical view\npatters such as getting an object by ID or returning a 404 error if not found.\n\n```python\n# views.py\n\nfrom .database import db, get_or_404\nfrom .models import User\n\n\n@bp.route("/")\ndef root():\n    users = db.session.query(User).all()\n    return render_template("index.html", users=users)\n\n\n@bp.route("/user/<int:user_id>")\ndef profile(user_id):\n    user = get_or_404(User, user_id)\n    return render_template("profile.html", user=user)\n```\n\nYou can adjust alembic\'s `env.py` file to get the database URL from you app\'s\nconfiguration:\n\n```python\n# migrations/env.py\n\nfrom my_flask_app.app import create_app\nfrom my_flask_app.database import Base\nfrom sqlalchemy_helpers.flask_ext import get_url_from_app\n\nurl = get_url_from_app(create_app)\nconfig.set_main_option("sqlalchemy.url", url)\ntarget_metadata = Base.metadata\n\n# ...rest of the env.py file...\n```\n\nAlso set `script_location` in you alembic.ini file in order to use it with the\n`alembic` command-line tool:\n\n```python\n# migrations/alembic.ini\n\n[alembic]\nscript_location = %(here)s\n```\n\n### Full example\n\nIn Fedora Infrastructure we use [a cookiecutter\ntemplate](https://github.com/fedora-infra/cookiecutter-flask-webapp/) that\nshowcases this Flask integration, feel free to check it out or even use it if\nit suits your needs.\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/fedora-infra/sqlalchemy-helpers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
