from .extrator import Extrator

class Descritor(Extrator):


    def candidaturaLivre(self):
        #Busca as candidaturas livres
        cl = self.df.loc[self.df['Candidatura']=='Candidatura Livre']
        if len(cl)==0:
            print('NÃO HÁ CANDIDATURAS LIVRES DISPONÍVEIS')
        else:
            return cl

    def candidaturaPaga(self):
        #Busca as candidaturas pagas
        cp = self.df.loc[self.df['Candidatura']=='Candidatura Paga']
        if len(cp)==0:
            print('NÃO HÁ CANDIDATURAS PAGAS')
        else:
            return cp

    def homeOffice(self):
        #Busca o trabalho home_office
        ho = self.df.loc[self.df['Forma de Trabalho']=='Home Office']
        if len(ho)==0:
            print('NÃO HÁ CANDIDATURAS QUE PERMITEM TRABALHO HOMEOFFICE')
        else:
            return ho

    def presencial(self):
        #Busca o trabalho Presencial
        pr = self.df.loc[self.df['Forma de Trabalho']=='Trabalho Presencial']
        if len(pr)==0:
            print('NÃO HÁ CANDIDATURAS QUE PERMITEM TRABALHO PRESENCIAL')
        else:
            return pr

    def combinar(self):
        #Busca salarios à combinar
        cb = self.df.loc[self.df['Salario']=='a combinar']
        if len(cb)==0:
            print('AS CANDIDATURAS DISPONÍVEIS JÁ POSSUEM SALÁRIO DEFINIDO')
        else:
            return cb
