from setuptools import setup, find_packages

setup(name = "PthMsn-Server-v1.1",
      version = "1.0",
      description = "Python Messenger Server. Version 1.",
      author = "NukeDancer",
      author_email = "nukedancer@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
