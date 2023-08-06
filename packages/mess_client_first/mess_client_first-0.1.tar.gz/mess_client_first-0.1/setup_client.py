from setuptools import setup, find_packages

setup(name="mess_client_first",
      version="0.1",
      description="mess_client",
      author="Tatiana Kudryavtseva",
      author_email="lexta@list.ru",
      packages=find_packages(),
      install_requires=['PyQt5',
                        'sqlalchemy',
                        'pycryptodome',
                        'pycryptodomex']
      )
