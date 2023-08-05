from setuptools import setup, find_packages

setup(name='msg_serv_13-21',
      version='0.1.9',
      description='The server part of the course project "Messenger"',
      author='Kostitsyn Aleksandr',
      author_email='kostitsin.a@mail.ru',
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex'],
      include_package_data=True,
      )
