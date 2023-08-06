from distutils.core import setup

setup(
    name='Dynamo_tools',
    version='1.0.0',
    author='Nirakar Basnet',
    author_email='nirakarbasnet@gmail.com',
    scripts=['bin/make_table.py','bin/plot_cc.py','bin/recenter.py','bin/relion_make_descr.py','bin/split_table.py'],
    license='LICENSE.txt',
    description='Dynamo tools',
    long_description=open('README.txt').read(),
    install_requires=[
        "Starfile",
        "dynamotable",
    ],
)