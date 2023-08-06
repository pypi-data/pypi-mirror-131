===================
upgrade-marshmallow
===================


.. image:: https://img.shields.io/pypi/v/upgrade-marshmallow.svg
        :target: https://pypi.python.org/pypi/upgrade-marshmallow

.. image:: https://img.shields.io/travis/featureoverload/upgrade-marshmallow.svg
        :target: https://travis-ci.com/featureoverload/upgrade-marshmallow

.. image:: https://readthedocs.org/projects/upgrade-marshmallow/badge/?version=latest
        :target: https://upgrade-marshmallow.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Upgrade marshmallow is a tool to batch modify call expression with `marshmallow.fields.Field`.


* Free software: MIT license
* Documentation: https://upgrade-marshmallow.readthedocs.io.


Problem
-------

After upgrade **marshmallow>=3.10.0**,
the non-reserved arguments(e.g. title, description) should passing in by metadata argument.

**Otherwise, it will pop RemovedInMarshmallow4Warning(when running pytest).**

Duplicate
~~~~~~~~~

code structure:

.. code:: shell

  $ tree .
  .
  ├── requirements.txt  # marshmallow==3.3.0
  ├── schemas.py
  └── test_warning.py


example code(`schemas.py`):

.. code:: python

  from marshmallow import Schema
  from marshmallow import fields


  class FooSchema(Schema):
      name = fields.String(
          required=True,
          title='foo',
          description='foo name')
      relationship = fields.String(
          title='bar', description='foobar')


test code(`test_warning.py`):

.. code:: python

  from schemas import FooSchema


  def test_warn():
      INPUT = {
          'name': 'something',
          'relationship': 'others'
      }
      schema = FooSchema()
      data = schema.load(INPUT)
      assert data == INPUT


upgrade marshmallow and duplicate this problem:

.. code:: shell

  $ pip install -U marshmallow
  ...
  Successfully installed marshmallow-3.14.1

  $ pytest test_warning.py
  ================== test session starts ================================
  platform darwin -- Python 3.8.3, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
  rootdir: /private/tmp/_
  collected 1 item                                                                                                                                     

  test_warning.py .                                                                                                                              [100%]

  ================== warnings summary =================================
  .venv/lib/python3.8/site-packages/marshmallow/fields.py:218
  /private/tmp/_/.venv/lib/python3.8/site-packages/marshmallow/fields.py:218: RemovedInMarshmallow4Warning: Passing field metadata as keyword arguments is deprecated. Use the explicit `metadata=...` argument instead. Additional metadata: {'title': 'foo', 'description': 'foo name'}
  warnings.warn(

  .venv/lib/python3.8/site-packages/marshmallow/fields.py:218
  /private/tmp/_/.venv/lib/python3.8/site-packages/marshmallow/fields.py:218: RemovedInMarshmallow4Warning: Passing field metadata as keyword arguments is deprecated. Use the explicit `metadata=...` argument instead. Additional metadata: {'title': 'bar', 'description': 'foobar'}
  warnings.warn(

  -- Docs: https://docs.pytest.org/en/stable/warnings.html
  ================== 1 passed, 2 warnings in 0.03s ===================



Issue
~~~~~

In some projects, we may use a lot of Field with `"title"`, `"description"` etc. arguments.

**It will take lots of effort to change each one by one manually**, 
and it's not easy to "replace" by editor tools or use **awk/sed**.


Solution
--------

**upgrade-marshmallow** use AST to parsing source code, then replacing arguments with expected code.


Features
--------

**upgrade-marshmallow** tool could handler many cases.

1. the most common(simple) way to use marshmallow.fields.Field:


  .. literalinclude:: ../tests/samples/most_common/schemas.py
     :language: python


2. alias fields:

  .. literalinclude:: ../tests/samples/alias_fields/schemas.py
     :language: python


3. `import marshmallow`, using Field with absolute path:

  .. literalinclude:: ../tests/samples/absolute/schemas.py
     :language: python


4. alias marshmallow:

  .. literalinclude:: ../tests/samples/alias_absolute/schemas.py
     :language: python


5. directly import to Field

  .. literalinclude:: ../tests/samples/field_func/schemas.py
     :language: python

6. rename `default` to `dump_default`, `missing` to `load_default`

  .. literalinclude:: ../tests/samples/default_missing/schemas.py
     :language: python
