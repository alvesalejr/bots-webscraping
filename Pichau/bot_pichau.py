import requests
from bs4 import BeautifulSoup
from loguru import logger
import json
import os 
import subprocess

# Uma função para fazer a requisição HTTP e obter o conteúdo HTML da página
# Uma função para extrair as informações de cada placa de vídeo do HTML
# Uma função para salvar as informações extraídas em um arquivo JSON


class BotPichau:

    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    url = 'https://www.pichau.com.br/hardware/placa-de-video'

    def __init__(self):  #Inicialização do BEATIFULSOUP
        self.create_dir()
        for i in range(4):
            print(i)
            
            if i == 0:
                soup = self.inicialize_bs4(self.url)
            else:
                soup = self.inicialize_bs4(self.url + f"?page={i}")
        
            itens = self.parse(soup)
        self.create_superjson()

    def inicialize_bs4(self, url):  # Inicialização do BEATIFULSOUP
        site = requests.get(url, self.headers)
        return BeautifulSoup(site.content, 'html.parser')

    def parse(self, site): # Função que tá trazendo as informações que eu quero.
        try:
            placas = site.find_all('div', class_='MuiCardContent-root jss62')
            for site in placas: # Condional
                marca = site.find('h2', class_='MuiTypography-root jss76 jss77 MuiTypography-h6').get_text().strip()
                preco = site.find('div', class_='jss79').get_text().strip()
                precocartao = site.find('div', class_='jss91').get_text().strip()
                
                if preco == None:
                    preco = 'Esgotado'
                if precocartao == None:
                    precocartao = 'Esgotado'

                self.formate_dict(marca, preco, precocartao) # Está retornando o dict das placas;
        except Exception as e:
            print(e)
            
    def formate_dict(self, marca, preco, precocartao): # Criando um DIct com as informações que eu quero do site
        placas = {
            'marca': marca,
            'preco': preco,
            'precocartao': precocartao      
        }
        
        self.save_file(placas)
    
    def save_file(self, placas): # Salvando as informações
        try: 
            with open(f'Pichau/jsons/{placas["marca"]}.json', 'w', newline='', encoding='UTF-8') as f:
                f.write(json.dumps(placas))
        except Exception as e:
            print(e)
    
    def create_superjson(self): 
        jsonzinhos = '{"placas": {'
        for file in os.listdir('Pichau/jsons'):
            with open('Pichau/jsons/' + file) as f:
                lines = f.read()
                lines = lines[1:]
                lines = lines[:-1]
                jsonzinhos += lines + ","
        jsonzinhos = jsonzinhos[:-1]
        jsonzinhos += "}}"
        with open('Pichau/placas.json', 'w') as f:
            f.write(jsonzinhos)
            
    def create_dir(self):
        if not os.path.exists('jsons'):
            subprocess.call('mkdir -p Pichau/jsons', shell = True)
            
if __name__ == '__main__':
    b = BotPichau()