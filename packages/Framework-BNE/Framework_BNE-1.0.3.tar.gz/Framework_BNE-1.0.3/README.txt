**BNEFramework**
* O Framework tem como objetivo auxiliar os brasileiros que estao a procura de emprego a localizarem de maneira mais pratica e concisa vagas que lhe interessem, alem de apresentar as vagas com candidaturas livres disponiveis no site do BNE(Banco Nacional de Emprego)'

**Funcoes do extrator**
* def prox_pag(self, n_paginas=6): -Essa funcao faz a passagem das paginas

* def extrair_infos(self): -Essa funcao extrai as informacoes presentes em cada pagina

* def salvar_csv(self, nome ,sep =','): -Essa funcao ira criar um df com as informacoes e salva-las em um arquivo .csv

**Funcoes do descritor**

* def candidaturaLivre(self): -Essa funcao, presente no descritor, separa apenas as candidaturas livres-IMPORTANTE: Em caso de nao existencia de pedidos pela funcao atributos o Framework retornara uma mensagem de aviso ao usuario

* def candidaturaPaga(self): -Essa funcao, presente no descritor, separa apenas as candidaturas pagas-IMPORTANTE: Em caso de nao existencia de pedidos pela funcao atributos o Framework retornara uma mensagem de aviso ao usuario

* def homeOffice(self): -Essa funcao, presente no descritor, separa apenas as vagas -IMPORTANTE: Em caso de nao existencia de pedidos pela funcao atributos o Framework retornara uma mensagem de aviso ao usuario

* def presencial(self): -Essa funcao, presente no descritor, separa apenas as vagas presenciais-IMPORTANTE: Em caso de nao existencia de pedidos pela funcao atributos o Framework retornara uma mensagem de aviso ao usuario

* def combinar(self): -Essa funcao, presente no descritor, separa apenas os salarios a combinar-IMPORTANTE: Em caso de nao existencia de pedidos pela funcao atributos o Framework retornara uma mensagem de aviso ao usuario
