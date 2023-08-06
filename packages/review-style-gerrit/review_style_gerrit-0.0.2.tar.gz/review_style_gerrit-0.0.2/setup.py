import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='review_style_gerrit',
    url='https://github.com/tom-010/review_style_gerrit',
    version='0.0.2',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['review_style_gerrit'], # find_packages(),
    license='Apache2',
    install_requires=[
        'gerrit-review-robot',
        'pylama[all]',
        'easy_exec'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Executes pylama and reports the result of the lines that are in the current diff to gerrit.',
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': [
            'review_style_gerrit = review_style_gerrit:main',
        ] 
    },
)