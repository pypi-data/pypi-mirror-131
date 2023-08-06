from setuptools import setup, find_packages

setup(name="Messenger_server_dmitry_vokh",
      version="1.0.0",
      description="mess_server",
      author="Dmitry Vokhmin",
      author_email="box@ya.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
