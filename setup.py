import os
try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Extension


#src_folder= os.path.join(
#    os.path.split(os.path.abspath(__file__))[0], 'src')

setup(
    name='tvdir',
    version="0.1.0",
    description='TV Directory',
    author='Diego Bendersky',
    #author_email='',
    url='',
    install_requires=[
            'django==1.4',
            'beautifulsoup4',
            'pyyaml',
            'psycopg2',
            'south',
            'simplejson',
            #'mechanize'
    ],
    tests_require=[
            'nose',
            ],
    include_package_data=True,
    packages=['tvdir'],  #find_packages(where=src_folder, exclude=['*.tests', '*.tests.*']),
    extras_require = {
    },
    #ext_package='pycommons',
    #ext_modules=[Extension("procname", [os.path.join('src', 'utils', 'procnamemodule.c')])],
    test_suite='nose.collector',
    #entry_points={
    #    'console_scripts':
    #    ['s3cleaner = utils.s3cleaner:main'],
    #},

    zip_safe=True
)


