from setuptools import setup, find_packages

setup(name = "PthMsn-Client-v1",
      version = "1.0",
      description = "Python Messenger Client. Version 1.",
      author = "NukeDancer",
      author_email = "nukedancer@yandex.ru",
      packages=find_packages(),      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
