import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='easy_exec',
    url='https://github.com/tom-010/easy_exec',
    version='0.0.1',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['easy_exec'],
    license='Apache2',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='A simple `exec` method to run system commands and geht `stdout`, `stderr` and `has_error`',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3',
)