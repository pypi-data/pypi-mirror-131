import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name='cmp-sdk',
    version='1.0.14',
    description='cmp sdk',
    long_description=README,
    long_description_content_type='text/markdown',
    url='',
    author='quwan',
    author_email='Csjs1-2@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['cmp_sdk'],
    include_package_data=True,
    install_requires=['requests', 'python-dateutil', 'requests','bumpversion'],
    entry_points={
    },
)
