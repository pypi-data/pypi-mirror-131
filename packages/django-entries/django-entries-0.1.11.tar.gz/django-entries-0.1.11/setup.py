# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entries', 'entries.migrations', 'entries.tests']

package_data = \
{'': ['*'],
 'entries': ['docs/*',
             'static/css/*',
             'static/img/favicons/*',
             'templates/*',
             'templates/base_template/*',
             'templates/entries/*']}

install_requires = \
['Django>=4.0,<5.0',
 'Markdown>=3.3.6,<4.0.0',
 'bleach>=4.1.0,<5.0.0',
 'django-crispy-forms>=1.13.0,<2.0.0',
 'django-extensions>=3.1.5,<4.0.0',
 'markdownify>=0.10.0,<0.11.0',
 'types-Markdown>=3.3.8,<4.0.0',
 'types-bleach>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'django-entries',
    'version': '0.1.11',
    'description': 'Entries is a helper Django app with CRUD functions based on htmx.',
    'long_description': '# django-entries\n\n## Overview\n\nBasic create-read-update-delete (CRUD) functionality for an `Entry` model.\n\nThe base [template](./entries/templates/base.html) makes use of light css and javascript:\n\n1. `starter.css` [stylesheet](./entries/static/css/starter.css)\n2. `pylon` 0.1.1 for `<hstack>` and `<vstack>` layouts\n3. `htmx` 1.6.1 for html-over-the-wire functionality, e.g. [infinite scrolling](./entries/docs/infinity_scroll.md)\n4. `hyperscript` 0.9 for client-side reactivity\n5. `simplemde` a simple markdown editor\n\n## Quickstart\n\nInstall in your virtual environment:\n\n```zsh\n.venv> pip3 install django-entries # poetry add django-entries\n```\n\nInclude package in main project settings file:\n\n```python\n# in project_folder/settings.py\nINSTALLED_APPS = [\n    ...,\n    \'crispy_forms\',  # add crispy_forms at least > v1.13, if not yet added\n    \'entries\' # this is the new django-entries folder\n]\n\n# in project_folder/urls.py\nfrom django.views.generic import TemplateView\nfrom django.urls import path, include # new\nurlpatterns = [\n    ...,\n    path(\'entry/\', include(\'entries.urls\')), # new\n    path("", TemplateView.as_view(template_name="home.html")), # (optional: if fresh project install)\n]\n```\n\nAdd to database:\n\n```zsh\n.venv> python manage.py migrate # adds the `Entry` model to the database.\n.venv> python manage.py createsuperuser # (optional: if fresh project install)\n```\n\nLogin to add:\n\n```zsh\n.venv> `python manage.py runserver`\n# Visit http://127.0.0.1:8000/entry/entries/list\n# Assumes _entry_ as folder in config/urls.py\n# The `Add entry` button is only visible to logged in users.\n# Can login via admin using the superuser account http://127.0.0.1:8000/admin/\n# Visit the list page again at http://127.0.0.1:8000/entry/entries/list to see the `Add entry` button.\n```\n\n## Test\n\n```zsh\n.venv> pytest --ds=config.settings --cov\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/justmars/django-entries',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
