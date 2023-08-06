from setuptools import setup, find_packages

setup(name="mess_server_proj_nortsev",
      version="0.0.1",
      description="Client-server apllication",
      author="Nortsev Vladimir",
      author_email="nortsev1989@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
