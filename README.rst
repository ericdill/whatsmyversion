``whatsmyversion``
--------------
Single module python package to make versioning simple.  You add a couple of
configuration parameters to your top-most python module and ``whatsmyversion`` will
determine the version string based on your git history.

Using ``whatsmyversion``
~~~~~~~~~~~~~~~~~~~~

Add the following to the top level of your package (package_name/__init__.py
or single_module_package.py) ::

    import whatsmyversion
    __version__ = whatsmyversion.version(__file__)
    del whatsmyversion

Add the following to your setup.py ::

    import package_name

    setup = (
        version = package_name.__version__
        ...
    )

Aaaaand that's it! ::

    python -c "import package_name; print(package_name.__version__)"

For example, look at the ``setup.py`` and ``whatsmyversion.py`` of this project for
guidance in setting up your own project! ::

    $ python -c "import whatsmyversion; print(whatsmyversion.__version__)"
    v0.0.2.post6+g32c6562

Configuring ``whatsmyversion``
~~~~~~~~~~~~~~~~~~~~~~~~~~
There are a few configuration options that you can provide to the `version`
function. These are:

``version_prefix`` which is defaults to ``v``

``version_suffix`` which is one of ``a``, ``b``, ``rc``, ``.post``, ``.dev``
and defaults to ``.post``

``use_local_version_id`` which is a boolean flag to include (True) or not
(False) the git hash and defaults to ``True`` because information is power

These three configuration options combine to produce a PEP440 compliant
version string. `PEP440 <https://www.python.org/dev/peps/pep-0440/>`_

Use cases
~~~~~~~~~

Working:

* Determine the version of a git repository

    * Installed with ``setup.py develop``

    * Installed with ``setup.py install``

Not yet working:

- Determine the version of source code downloaded from github
