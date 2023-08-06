# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comments', 'comments.migrations', 'comments.templatetags']

package_data = \
{'': ['*'],
 'comments': ['docs/*',
              'static/css/*',
              'static/img/favicons/*',
              'templates/*',
              'templates/base_template/*',
              'templates/comments/*']}

install_requires = \
['Django>=4.0,<5.0',
 'django-crispy-forms>=1.13.0,<2.0.0',
 'django-extensions>=3.1.5,<4.0.0']

setup_kwargs = {
    'name': 'django-add-comments',
    'version': '0.0.5',
    'description': 'Add and display htmx comments to arbitrary Django models.',
    'long_description': '# django-add-comments\n\nAdd `comments` to a Django model via mixin:\n\n```python\n# app/models.py\nfrom comment.models import AbstractCommentable # import mixin\nclass Sentinel(AbstractCommentable): # add to class declaration\n    """Any `app`, e.g. `essay`, `article`... can be \'commentable\'."""\n    title = models.CharField(max_length=50)\n```\n\n| Action                | Authorization       | Description                          |\n| --------------------- | ------------------- | ------------------------------------ |\n| View comments list    | All users           | Add filter public/private later      |\n| Get comment form      | Authenticated users | Reactive via htmx / hyperscript [^1] |\n| Delete / edit comment | Authorized authors  | Reactive via htmx / hyperscript [^1] |\n\n## Setup\n\n### Load virtual env\n\n```zsh\n.venv> poetry add django-add-comments # pip3 install django-add-comments\n```\n\nWill include dependencies from [pyproject.toml](../../pyproject.toml):\n\n```toml\npython = "^3.8"\nDjango = "^4.0"\ndjango-extensions = "^3.1.5"\ndjango-crispy-forms = "^1.13.0"\n```\n\n### Add app to project settings\n\n```python\n# in project_folder/settings.py\nINSTALLED_APPS = [\n    ...,\n    \'crispy_forms\',  # add crispy_forms at least > v1.13, if not yet added\n    \'comments\' # this is the new django-comments folder\n]\n```\n\n### Add basic routes to urlpatterns\n\n```python\n# in project_folder/urls.py\nfrom django.urls import path, include # new\nurlpatterns = [\n    ...,\n    path(\'comments/\', include(\'comments.urls\')) # routes for update, delete, view, toggle comment\n]\n```\n\n### Add Comment model to database\n\n```zsh\n.venv> python manage.py migrate\n```\n\n## Configuration\n\n### What we\'re going to do\n\n```zsh\n>>> obj = Sentinel.objects.create(title="A sample title") # instance is made, e.g. id=1, id=2, etc.\n>>> obj.add_comment_url # url to add a comment to `A sample title`\n```\n\nA sentinel is the model being commented on.\n\nWe\'ve created a dummy `Sentinel` model to represent this construct.\n\nLet\'s say we\'ve initialized one model instance called `obj` with `slug`="a-sample-title".\n\nWhat we\'d like is the ability to write a comment to `obj` through a url represented by: `obj.add_comment_url`\n\n`@add_comment_url` thus needs to become a property of the `Sentinel` model.\n\n### Add imports\n\n```python\n# sentinels/models.py\nfrom comments.models import AbstractCommentable # new\nfrom django.template.response import TemplateResponse # new\nfrom django.urls import reverse, URLPattern # new\nfrom django.utils.functional import cached_property, classproperty # new\n```\n\n### Make sentinel model inherit from abstract base model\n\n```python\n# sentinels/models.py\nclass Sentinel(AbstractCommentable): # new\n    ...\n```\n\n### Add model properties\n\n```python\n# sentinels/models.py\nclass Sentinel(AbstractCommentable):\n\n    id = models.UUIDField ... # identifier is UUID\n    slug = models.Slugfield ...\n\n    @cached_property # copy this to the sentinel model, note `slug` as identifier\n    def add_comment_url(self) -> str:\n        return self.set_add_comment_url(self.slug)\n\n    @classmethod # copy this to the sentinel model, note `slug` as identifier\n    def add_comment_func(cls, request, slug: str) -> TemplateResponse:\n        target = cls.objects.get(slug=slug)\n        return cls.allow_commenting_form_on_target_instance(request, target)\n\n    @classproperty # copy this to the sentinel model, note `slug` as identifier\n    def add_comment_path(cls) -> URLPattern:\n        return cls.set_add_comment_path("<slug:slug>", cls.add_comment_func)\n```\n\n_Gotcha_: if `pk` is identifier, revise `<slug:slug>` to `<pk:int>` above:\n\n1. `self.set_add_comment_url(app_name, self.pk)`\n2. `def add_comment_func(cls, request, pk: int):`\n3. `target = cls.objects.get(pk=pk)`\n4. `cls.set_add_comment_path("<pk:int>", cls.add_comment_func)`\n\n### Add sentinel namespaced url for adding comments\n\nAdd path to the sentinel\'s url patterns:\n\n```python\n# sentinels/urls.py\nfrom .models import Sentinel\nfrom .apps import SentinelConfig # already pre-made during `python manage.py startapp sentinels`\napp_name = SentinelConfig.name # remember the `app_name` in relation to the `add_comment_url` property\nurl_patterns = [\n    Sentinel.add_comment_path, # This is really just a shortcut to a created path.\n    ...\n]\n```\n\n### Add template tag for displaying comment form with list of added comments\n\nAdd template tag to sentinel\'s template to show form with list\n\n```jinja\n<!-- sentinels/templates/sentinel_detail.html -->\n<h1>Title: {{ obj.title }}</h1>  <!-- the `obj` is whatever variable passed to the template -->\n{% load comments %} <!-- see templatetags/comments.py which contains `object.add_comment_url`  -->\n{% list_comments obj %}\n```\n\nThe form that represents this "add comment" action / url will be loaded in every comment list. See context in [template tag](../templatetags/comments.py).\n\n[^1]: [No page refresh](./comments/docs/frontend.md)\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/justmars/django-add-comments',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
