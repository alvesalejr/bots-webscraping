#Robô que usa a biblioteca BeautifulSoup para extrair links de imagens do site da NASA, baixar as imagens e salvar em um diretório local;
import requests
from bs4 import BeautifulSoup
import os
from datetime import date, timedelta


class bot_fabrica:  
     
    save_dir = 'Desafio/Imagens' 

    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    url = 'https://apod.nasa.gov/apod/'
    
    def __init__(self): #Este método inicializa o raspador de página, cria o diretório de saída e raspa cinco páginas;
        self.makedir()
        for counter in range(5):  #Itera(Percorre) por cinco vezes para baixar cinco páginas do site;
            url = self.url_create(counter) 
            site = requests.get(url, headers=self.headers) 
            self.parse_page(site)  
       
    def url_create(self, counter_day): #Este método (Função) calcula a data atual, formata pro formato certo e cria uma URL completa para a data especificada;
        data = date.today() - timedelta(days=counter_day) 
        data_formatada = self.date_sanitize(data) 
        url_parse = self.url+ 'ap' +data_formatada + '.html'  
        
        return url_parse  
    
    def date_sanitize(self, data): # Este método (Função) calcula a data atual e formata pro formato adequado;
        year = str(data.year)[2:] 
        day = str(data.day) 
        
        if len(day)==1: 
            day = '0'+ day
        
        return f'{year}{data.month}{day}' 
    
    def parse_page(self, response): # Este método (Função) é a que percorre pelo site e processa o conteúdo;
        link = []  
        soup = BeautifulSoup(response.content, 'html.parser')  
        for a in soup.find_all(href = True): 

            link.append(a['href']) #Adiciona o link a lista ARRAY;
        image_link = self.url + link[1] 
        self.download_image(image_link) 

    def download_image(self, image):
        response = requests.get(image) #Faz uma requisição para baixar a imagem;
        filename = image.split('/')[-1]  
        self.save_image(filename, response) 

        
    def save_image(self, filename, response): 
        with open(f'{self.save_dir}/{filename}', 'wb') as imagem:  
            imagem.write(response.content) 
            
    def makedir(self): #Função que cria que o diretório das imagens;
        if not os.path.exists(self.save_dir):  
         os.makedirs(self.save_dir)
         
if __name__ == '__main__': 
    bot = bot_fabrica() 