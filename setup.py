from setuptools import setup

setup(
    name='extractor_api',
    packages=['extractor_api'],
    include_package_data=True,
    install_requires=[
    'requests',
    'pandas',
    'simplejson',
    'matplotlib',
    ],
    scripts=[
        'bin/load_extapi',
    ]
)
