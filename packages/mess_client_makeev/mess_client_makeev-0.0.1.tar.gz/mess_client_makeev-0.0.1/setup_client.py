from setuptools import setup, find_packages

setup(name="mess_client_makeev",
      version="0.0.1",
      description="mess_client_makeev",
      author="Eduard Makeev",
      author_email="",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
