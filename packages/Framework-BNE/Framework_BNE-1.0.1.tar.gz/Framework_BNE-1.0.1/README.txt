**BNEFramework** 
* O Framework tem como objetivo auxiliar os brasileiros que estão a procura de emprego a localizarem de maneira mais prática e concisa vagas que lhe interessem, além de apresentar as vagas com candidaturas livres disponíveis no site do BNE(Banco Nacional de Emprego)'

**Funções do extrator**
* def prox_pag(self, n_paginas=6): -Essa função faz a passagem das páginas

* def extrair_infos(self): -Essa função extrai as informações presentes em cada página

* def salvar_csv(self, nome ,sep =','): -Essa função irá criar um df com as informações e salvá-las em um arquivo .csv

**Funções do descritor**

* def candidaturaLivre(self): -Essa função, presente no descritor, separa apenas as candidaturas livres-IMPORTANTE: Em caso de não existência de pedidos pela função atributos o Framework retornará uma mensagem de aviso ao usuário

* def candidaturaPaga(self): -Essa função, presente no descritor, separa apenas as candidaturas pagas-IMPORTANTE: Em caso de não existência de pedidos pela função atributos o Framework retornará uma mensagem de aviso ao usuário

* def homeOffice(self): -Essa função, presente no descritor, separa apenas as vagas -IMPORTANTE: Em caso de não existência de pedidos pela função atributos o Framework retornará uma mensagem de aviso ao usuário

* def presencial(self): -Essa função, presente no descritor, separa apenas as vagas presenciais-IMPORTANTE: Em caso de não existência de pedidos pela função atributos o Framework retornará uma mensagem de aviso ao usuário

* def combinar(self): -Essa função, presente no descritor, separa apenas os salários à combinar-IMPORTANTE: Em caso de não existência de pedidos pela função atributos o Framework retornará uma mensagem de aviso ao usuário
