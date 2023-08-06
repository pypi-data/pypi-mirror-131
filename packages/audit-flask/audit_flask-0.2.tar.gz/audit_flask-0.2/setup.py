import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent


VERSION = 0.2
PACKAGE_NAME = 'audit_flask'
AUTHOR = 'José Luis Rosales Meza'
AUTHOR_EMAIL = 'jrosalesmeza@gmail.com'
URL = 'https://github.com/jrosalesmeza/audit_flask'

LICENSE = 'MIT'
DESCRIPTION = 'Libreria para realizar auditoria a modelos de Mongo y Postgres'
LONG_DESCRIPTION = (HERE / "README.MD").read_text(encoding= 'utf8')
LONG_DESC_TYPE = 'text/markdown'

INSTALL_REQUIRES = [
                'flask',
                'mongoengine',
                'blinker',
                'sqlalchemy'
            ]

setup(
    name = PACKAGE_NAME,
    version = VERSION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = LONG_DESC_TYPE,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    url = URL,
    install_requires = INSTALL_REQUIRES,
    license = LICENSE,
    packages= find_packages(),
    include_package_data= True
)