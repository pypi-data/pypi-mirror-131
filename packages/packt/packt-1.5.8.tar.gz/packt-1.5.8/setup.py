import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

package_version = '1.5.8'

requirements = [
    'click==8.0.3',
    'google-api-python-client==2.27.0',
    'oauth2client==4.1.3',
    'requests==2.26.0',
    'python-slugify==5.0.2 '
]

dev_requirements = [
    'bumpversion==0.5.3',
    'mccabe==0.6.1',
    'pycodestyle==2.8.0',
    'pyflakes==2.4.0',
    'pylama==7.7.1'
]

setup(
    name='packt',
    version=package_version,
    packages=find_packages(),
    license='MIT',
    description='Script for grabbing daily Packt Free Learning ebooks',
    author='Łukasz Uszko',
    author_email='lukasz.uszko@gmail.com',
    url='https://gitlab.com/packt-cli/packt-cli',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['packt'],
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    entry_points={
        'console_scripts': [
            'packt-cli = packt.packtPublishingFreeEbook:packt_cli',
        ],
    },
    download_url='https://gitlab.com/packt-cli/packt-cli/-/archive/v1.5.8/packt-cli-v1.5.8.tar.gz',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)
