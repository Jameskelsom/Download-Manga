import requests
import os
from bs4 import BeautifulSoup #atualizado
import re
from tqdm import tqdm #progressbar
import requests_cache #criar o cache de todos os requests

requests_cache.install_cache('DownloadManga_cache')

class downloadManga:
    def setUp(self, manga):
        self.url_base = 'http://centraldemangas.online'
        self.displayMsg('Manga', manga.lower().capitalize())
        manga = manga.replace(' ', '-').lower()
        self.searchManga(manga)

    def createDirectory(self):
        try:
            os.mkdir(self.manga) #criar pasta
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
                self.createDirectory()
                self.descriptionManga()
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
        self.downloadImg(capa,self.manga,'')

    def loadLinks(self): #carregando todos os links
        links=[]
        [links.append(link['href']) for link in self.bs.find_all(href=re.compile('/titulos/'))]
        for i in tqdm(range(len(links))):
            url = self.url_base + links[i]
            response = requests.get(url)
            bs  = BeautifulSoup(response.text,'html.parser')
            itens = len(bs.find_all('script'))-1
            i = len((bs.find_all('script')[itens].get_text()).split())-1
            parm = (bs.find_all('script')[itens].get_text()).split()
            urlSulfix = parm[15].replace("'","").replace(';','')
            pages = parm[i-1]

            for char in "'[];":
                pages = pages.replace(char,'')

            for page in pages[:-1].split(','):
                urlImg = urlSulfix + page +'.jpg'
                self.downloadImg(url,self.manga,urlImg)
    
    def downloadImg(self,url,manga,urldownload): #download das imagens
        if len(urldownload)==0:
            response = requests.get(url)
            if response.status_code == 200:
                with open(manga +"/capa.jpg", 'wb') as f:
                    f.write(response.content)
                    print('Download da capa!!!')
        else:
            headers = {
                        'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36 OPR/65.0.3467.78',
                        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                        'Referer': url,
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                        }
            response = requests.get(urldownload, headers=headers, verify=False)
            mangaSplit = urldownload.split('/')
            mangaImg = mangaSplit[len(mangaSplit)-1]
            with open(manga +"/" + mangaImg, 'wb') as f:
                    f.write(response.content)

manga = str(input('Digite o nome do manga: '))
d = downloadManga()
d.setUp(manga)
