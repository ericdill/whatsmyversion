theversion
----------
Single module python package to make versioning simple.  You add a couple of
configuration parameters to your top-most python module and `theversion` will
determine your git version string

Using `theversion`
~~~~~~~~~~~~~~~~~~

Add the following to the top level of your package (package_name/__init__.py
or single_module_package.py) ::

    import theversion
    __version__ = theversion.version(__file__)
    del theversion

Add the following to your setup.py

    import package_name

    setup = (
        version = package_name.__version__
    )

Aaaaand that's it!



Use cases
~~~~~~~~~

Working:

1. Determine the version of a git repository

    1. Installed with `setup.py develop`
    1. Installed with `setup.py install`

Not yet working:
1. Determine the version of source code downloaded from github
