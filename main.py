"""
Uso de Threads em Python em uma aplicação de Processamento de Imagens, que envolve o Realce de Imagens em Nível de Cinza.

Ao todo são criadas duas novas threads com as seguintes funções:
    -> Thread 1: Alargamento de Contraste; 
    -> Thread 2: Equalização de Histograma

Essa atividade faz parte da disciplina DCA0108 - Sistemas Operacionais ministrada pelo prof. Diogo Pinheiro.

Autores:
    -> Gilvandro César;
    -> Marcos Henrique;
    -> Renato Lins.
"""
from PIL import Image
import numpy as np
import threading
import time

# Classe para execução da thread responsável pelo Alargamento de Contraste
class AlargamentoDeContraste (threading.Thread):
    # Inicializador da classe AlargamentoDeContrate que herda da classe threading.Thread
    def __init__(self, threadID,threadNome, img):
        threading.Thread.__init__(self)
        self._id = threadID
        self._nome = threadNome
        self._img = img

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        # Aviso do inicio da thread
        print('Iniciando a Thread {} [{}]'.format(self._id,self._nome))
        
        # Criando a matrix nula G com as dimensões e tipo da imagem original
        # G é a matrix que guardara os valores apos o alargamento de contraste
        G = np.zeros(self._img.shape, dtype = self._img.dtype)

        # Imax: valor da intensidade máxima da imagem original
        Imax = np.amax(self._img)

        # Imin: valor da intensidade mínina da imagem original
        Imin = np.amin(self._img)

        # Int_Contraste representa o intervalo de contraste
        Int_Contraste = Imax - Imin
        
        # Numero de linhas da imagem
        M = self._img.shape[0]
        # Numero de colunas da imagem
        N = self._img.shape[1]

        # Aplicando o Alargamento de Contraste
        for i in range(M):
            for j in range(N):
                G[i][j] = (255/Int_Contraste)*(self._img[i][j] - Imin)
        
        # Convertendo G para uma imagem da classe PIL
        img_g = Image.fromarray(G)
        # Salvando a imagem no formato png
        img_g.save("imagens/alargamento_de_contraste.png")
        
        # Aviso do fim da thread
        print('Fim da Thread {} [{}]'.format(self._id,self._nome))
   

# Classe para execução da thread responsável pelo Equalizacao de Histograma
class EqualizacaoDeHistograma (threading.Thread):
    # Inicializador da classe EqualizacaoDeHistograma que herda da classe threading.Thread
    def __init__(self, threadID,threadNome, img):
        threading.Thread.__init__(self)
        self._id = threadID
        self._nome = threadNome
        self._img = img

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        # Aviso do inicio da thread
        print('Iniciando Thread {} [{}]'.format(self._id,self._nome))

        # Numero de linhas da imagem
        M = self._img.shape[0]
        # Numero de colunas da imagem
        N = self._img.shape[1]

        # Difinindo o histograma para a imagem
        histograma = np.zeros(256, dtype = int)

        # Calculando o histrograma
        for i in range(M):
            for j in range(N):
                histograma[self._img[i][j]] += 1
        
        # Probabiliade de ocorrencia de cada nivel de cinza
        probabilidade_de_ocorrencia = np.zeros(256, dtype = float)

        # Calculando a probabiliade de ocorrencia de cada nivel de cinza
        for i in range(256):
            probabilidade_de_ocorrencia[i] = histograma[i]/(M*N)
        
        # Probabilidade Acumulada para cada pixel
        probabilidade_acumulada = np.zeros(256, dtype = float)

        probabilidade_acumulada[0] = probabilidade_de_ocorrencia[0]
        for i in range(1,256):
            probabilidade_acumulada[i] = probabilidade_acumulada[i-1] + probabilidade_de_ocorrencia[i]
        
        # Criando a matrix nula G com as dimensões e tipo da imagem original
        # G é a matrix que guardara os valores apos a equalizacao de histograma
        G = np.zeros(self._img.shape, dtype = self._img.dtype)
        
        for i in range(M):
            for j in range(N):
                G[i][j] = round(255*probabilidade_acumulada[self._img[i][j]])

        # Convertendo G para uma imagem da classe PIL
        img_g = Image.fromarray(G)
        # Salvando a imagem no formato png
        img_g.save("imagens/equalizacao_de_histograma.png")
        
        # Aviso do fim da thread
        print('Fim da Thread {} [{}]'.format(self._id,self._nome))


# Realizando a leitura da imagem
balloons_img = Image.open('imagens/balloons.png')

# Obtendo a matriz da imagem
ballonns_matrix = np.array(balloons_img)

# Instanciando um objeto da Thread Alargamento de Contraste
thread_alargamento_de_contraste = AlargamentoDeContraste(1,"Alargamento de Contraste",ballonns_matrix)

# Instanciando um objeto da Thread Equalizacao de Histograma
thread_equalizacao_de_histograma = EqualizacaoDeHistograma(2,"Equalizacao de Histograma",ballonns_matrix)

# Iniciando a Thread para o Alargamento de Contraste
thread_alargamento_de_contraste.start()

# Iniciando a Thread para Equalizacao de Histograma
thread_equalizacao_de_histograma.start()

# Esperando que a Thred de Alargamento de Contraste seja concluida
thread_alargamento_de_contraste.join()

# Esperando que a Thred de Equalizacao de Histograma seja concluida
thread_equalizacao_de_histograma.join()

