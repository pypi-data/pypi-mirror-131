import pathlib

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='dicio_scrapper',
    version='0.0.1',
    author='Data & Analytics Research',
    author_email='analytics.dar@take.net',
    packages=['dicio'],
    test_suite='tests',
    url='https://github.com/miloutsch/dicio',
    license='MIT License',
    description='Unofficial Python API for Dicio based on the original API of Felipe Pontes.',
    credits=['Felipe Pontes', 'Ramon Durães', 'Milo Utsch'],
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Utilities',
    ],
)
