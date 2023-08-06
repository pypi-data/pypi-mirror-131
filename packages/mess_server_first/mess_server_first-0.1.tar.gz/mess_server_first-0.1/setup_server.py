from setuptools import setup, find_packages

setup(name="mess_server_first",
      version="0.1",
      description="mess_server",
      author="Tatiana Kudryavtseva",
      author_email="lexta@list.ru",
      packages=find_packages(),
      install_requires=['PyQt5',
                        'sqlalchemy',
                        'pycryptodome',
                        'pycryptodomex']
      )

