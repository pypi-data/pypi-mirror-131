import os
import re
from setuptools import setup

requirements = [
    "astor>=0.8.1",
    "click>=8.0.3",
]

about = {}

pwd = os.path.dirname(__file__)

with open(os.path.join(pwd, 'upgrade_marshmallow', '__init__.py')) as f:
  VERSION = (
      re.compile(r""".*__version__ = ["'](.*?)['"]""", re.S)
      .match(f.read())
      .group(1)
  )


setup(
    name='upgrade_marshmallow',
    version=VERSION,
    url='https://github.com/featureoverload/upgrade-marshmallow',
    author='Feature Overload',
    author_email='featureoverload@gmail.com',
    maintainer='Feature Overload',
    maintainer_email='featureoverload@gmail.com',
    packages=['upgrade_marshmallow'],
    package_dir={'upgrade_marshmallow': 'upgrade_marshmallow'},
    entry_points={'console_scripts': ['ugma = upgrade_marshmallow.cli:main']},
    description=('Upgrade marshmallow is a tool to batch modify '
                 'call expression with "marshmallow.fields.Field".'),
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=requirements
)
