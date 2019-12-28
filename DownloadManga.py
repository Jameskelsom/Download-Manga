import requests
import os
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm

class downloadManga:
    def setUp(self, manga):
        self.url_base = 'http://centraldemangas.online'
        self.displayMsg('Manga', manga)
        manga = manga.replace(' ', '-')
        self.searchManga(manga)

   

    def downloadImg(self,url,manga):
        response = requests.get(url)
        if response.status_code == 200:
            with open(manga +"/capa.jpg", 'wb') as f:
                f.write(response.content)
                print('Download da capa!!!')

    def createDirectory(self):
        try:
            os.mkdir(self.manga)
        except:
            pass

    def searchManga(self, manga):
        self.manga = manga
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
                self.createDirectory()
                self.loadLinks()

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
        capa = bs.find(class_='ui relaxed list').find_all(class_='description')[0].find('img')['src']
        self.displayMsg('Descrição', descricao)
        self.displayMsg('Ano', ano)
        self.displayMsg('Arte', arte)
        self.displayMsg('Autor', autor)
        self.displayMsg('Gênero', genero)
        self.displayMsg('Status', status)
        self.downloadImg(capa,self.manga)

    def loadLinks(self):
        bs = self.bs
        self.driver = webdriver.Chrome()
        links=[]
        [links.append(link['href']) for link in bs.find_all(href=re.compile('/titulos/'))]
        for i in tqdm(range(len(links))):
            self.driver.get(self.url_base + links[i])

manga = str(input('Digite o nome do manga: '))
d = downloadManga()
d.setUp(manga)
