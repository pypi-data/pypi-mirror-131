from selenium import webdriver
import pandas as pd
from time import sleep

class Extrator:

    def __init__(self,caminho):
        self.driver = webdriver.Chrome(caminho)
        self.driver.get("https://www.bne.com.br/vagas-de-emprego-para-vendedor/?Page=1&Function=vendedor&Area=Com%C3%A9rcio&Sort=0")
        self.lista_local = []
        self.lista_salario = []
        self.lista_empresa = []
        self.lista_forma = []
        self.lista_candidatura = []
        self.intervalo_pags = 1
        self.df = pd.DataFrame()

        # Busca as informações
    def extrair_info(self):
        for z in range(1, 8):
            if z != 4:
                xpath_local = f'/html/body/div[5]/section/div[3]/div[{z}]/div[1]/dl[1]/dd'
                local = self.driver.find_element_by_xpath(xpath_local)
                self.lista_local.append(local.text)
                xpath_salario = f'/html/body/div[5]/section/div[3]/div[{z}]/div[1]/dl[2]/dd'
                salario = self.driver.find_element_by_xpath(xpath_salario)
                self.lista_salario.append(salario.text)
                xpath_empresa = f'/html/body/div[5]/section/div[3]/div[{z}]/div[1]/dl[3]/dd'
                empresa = self.driver.find_element_by_xpath(xpath_empresa)
                self.lista_empresa.append(empresa.text)
                try:
                    xpath_home_office = f'/html/body/div[5]/section/div[3]/div[{z}]/div[2]/h4[3]/span'
                    home_office = self.driver.find_element_by_xpath(xpath_home_office)
                    self.lista_forma.append(home_office.text)
                except:
                    self.lista_forma.append('Trabalho Presencial')
                try:
                    xpath_candidatura_livre = f'//*[@id="job-3206490"]/div[2]/h[{z}]'
                    candidatura_livre = self.driver.find_element_by_xpath(xpath_candidatura_livre)
                    self.lista_candidatura.append(candidatura_livre.text)
                except:
                    self.lista_candidatura.append('Candidatura Paga')

    #CLica na próxima página
    def prox_pag(self, n_paginas=6):
        for x in range(1,n_paginas+1):
            xpath_clique = f'//*[@id="pagination"]/ul/li[{x}]'
            clique = self.driver.find_element_by_xpath(xpath_clique)
            self.driver.execute_script("arguments[0].scrollIntoView()", clique)  # Scroll to element
            sleep(self.intervalo_pags)
            clique.click()
            self.extrair_infos()

            #self.driver.quit()


    def salvar_csv(self, nome ,sep =','):
        df = pd.DataFrame(
            {'Candidatura': self.lista_candidatura, 'Localização': self.lista_local, 'Salario': self.lista_salario,
             'Empresa': self.lista_empresa, 'Forma de Trabalho': self.lista_forma})
        df['Empresa'] = df['Empresa'].map(lambda x: x.lstrip('+-').rstrip('O que é isso?'))

        self.df = df
        self.df.to_csv(nome, sep = ',', index=False)
