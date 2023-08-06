from setuptools import setup
from Cython.Build import cythonize

setup(
    name="testin",
    ext_modules=cythonize("reciever.pyx"),
    zip_safe=False
)
