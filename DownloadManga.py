import requests
import os
from bs4 import BeautifulSoup


class downloadManga:
    def setUp(self, manga):
        self.url_base = 'http://centraldemangas.online'
        self.displayMsg('Manga', manga)
        manga = manga.replace(' ', '-')
        self.searchManga(manga)

    def createDirectory(self, manga):
        try:
            os.mkdir(manga)
        except:
            pass

    def searchManga(self, manga):
        r = requests
        url = self.url_base + '/titulos/' + manga
        response = r.get(url)
        if response.status_code == 200:
            self.bs = BeautifulSoup(response.text, 'html.parser')
            if len(self.bs.find_all(class_='ui message')) > 0:
                print('Página não encontrada')
                print(
                    'Esta página foi removida, não existe mais, ou talvez nunca tenha existido!')
            else:
                self.descriptionManga()
                self.createDirectory(manga)

        else:
            print('Pagina não encontrada!!!')
            print('Error: ' + str(response.status_code))

    def clearString(self, text):
        text = text.replace('\n', '')
        return text
    
    def clearStringGenero(self, text):
        text = text.replace('\n', ' | ')
        return text

    def displayMsg(self, tipo, text):
        print(tipo + ': ' + text)
        print('- -' * 20)
    
    def descriptionManga(self):
        bs = self.bs
        descricao = self.clearString(bs.find(class_='ui relaxed list').find(class_='description').get_text())
        ano = self.clearString(bs.find(class_='ui relaxed list').find_all(class_='description')[1].get_text())
        arte = self.clearString(bs.find(class_='ui relaxed list').find_all(class_='description')[2].get_text())
        autor = self.clearString(bs.find(class_='ui relaxed list').find_all(class_='description')[3].get_text())
        status = self.clearString(bs.find(class_='ui relaxed list').find_all(class_='description')[6].get_text())
        genero = self.clearStringGenero(bs.find(class_='ui relaxed list').find_all(class_='description')[4].get_text())
        self.displayMsg('Descrição', descricao)
        self.displayMsg('Ano', ano)
        self.displayMsg('Arte', arte)
        self.displayMsg('Autor', autor)
        self.displayMsg('Gênero', genero)
        self.displayMsg('Status', status)


manga = str(input('Digite o nome do manga: '))
d = downloadManga()
d.setUp(manga)
