from setuptools import setup, find_packages

setup(name="meeseng_server",
      version="0.0.1",
      description="meeseng_server",
      author="Simakin Sergey",
      author_email="sergeysimakin@gmail.com",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
