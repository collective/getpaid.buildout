from setuptools import setup

setup(
    name="recipes",
    version="0.0.1",
    entry_points={'zc.buildout': ['cleanup = cleanup:Cleanup']},
    install_requires = [ 'getpaid.core' ],
    )
