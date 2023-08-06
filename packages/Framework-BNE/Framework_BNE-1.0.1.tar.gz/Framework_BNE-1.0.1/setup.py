from setuptools import setup

setup(
    name = 'Framework_BNE',
    version = '1.0.1',
    author = 'Beatriz Rodovalho, Eduardo Furlani, Gabriel Benga, Lucas Gregório, Thiago Melo',
    author_email = 'dudufurlani58@gmail.com',
    packages = ['Extrator_bne'],
    url = 'https://github.com/edufurlani/BNE/tree/main',

    license = 'MIT',

    keywords = 'BNE',

    long_description=open('README.txt').read(),

    description= u'O Framework tem como objetivo auxiliar os brasileiros que estão a procura de emprego a localizarem de maneira mais prática e concisa vagas que lhe interessem, além de apresentar as vagas com candidaturas livres disponíveis no site do BNE(Banco Nacional de Emprego)'

)
