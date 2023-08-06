from setuptools import setup, find_packages

setup(name="mrz_mess_client",
      version="0.0.1",
      description="mess_client",
      author="morozov1982",
      author_email="morozov1982@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
