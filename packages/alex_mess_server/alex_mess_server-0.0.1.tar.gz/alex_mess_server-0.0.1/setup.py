from setuptools import setup, find_packages
setup(name="alex_mess_server",
      version="0.0.1",
      description="my_mess_server",
      author="Alexandr Pogrebnyak",
      author_email="cool.cyclon@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
