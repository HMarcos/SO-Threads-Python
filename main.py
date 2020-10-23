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
import matplotlib.pyplot as plt

# Classe para execução da thread responsável pelo Alargamento de Contraste
class AlargamentoDeContraste (threading.Thread):
    # Inicializador da classe AlargamentoDeContrate que herda da classe threading.Thread
    def __init__(self, threadID,threadNome, img):
        threading.Thread.__init__(self)
        self._id = threadID
        self._nome = threadNome
        self._img = img
        self._img_g = None
        self._tempo_de_execucao = 0

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        
        # Marca o inicio da execucao da thread
        thread_ac_inicio = time.time()

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
        
        self._img_g = img_g

        # Mostrando a imagem apos o alargamento de contraste
        #img_g.show()
                
        # Aviso do fim da thread
        print('Fim da Thread {} [{}]'.format(self._id,self._nome))
        # Marca o fim da execucao da thread
        thread_ac_fim = time.time()
        # Tempo de execucao da thread
        self._tempo_de_execucao = thread_ac_fim - thread_ac_inicio
   

# Classe para execução da thread responsável pelo Equalizacao de Histograma
class EqualizacaoDeHistograma (threading.Thread):
    # Inicializador da classe EqualizacaoDeHistograma que herda da classe threading.Thread
    def __init__(self, threadID,threadNome, img):
        threading.Thread.__init__(self)
        self._id = threadID
        self._nome = threadNome
        self._img = img
        self._img_g = None
        self._tempo_de_execucao = 0

    # a funcao run() e executada por padrao por cada thread
    def run(self):
        
        # Marca o inicio da execucao da thread
        thread_eh_inicio = time.time()
        
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
        
        self._img_g = img_g

        # Mostrando a imagem apos a equalizacao de histograma
        #img_g.show()
        
        # Aviso do fim da thread
        print('Fim da Thread {} [{}]'.format(self._id,self._nome))
        
        # Marca o fim da execucao da thread
        thread_eh_fim = time.time()
        # Tempo de execução da thread
        self._tempo_de_execucao = thread_eh_fim - thread_eh_inicio


if __name__ == "__main__":
    # Marca o inicio do programa
    inicio_do_programa = time.time()
    # Realizando a leitura da imagem
    balloons_img = Image.open('imagens/balloons.png')

    # Obtendo a matriz da imagem
    balloons_matrix = np.array(balloons_img)

    # Instanciando um objeto da Thread Alargamento de Contraste
    thread_alargamento_de_contraste = AlargamentoDeContraste(1,"Alargamento de Contraste",balloons_matrix)

    # Instanciando um objeto da Thread Equalizacao de Histograma
    thread_equalizacao_de_histograma = EqualizacaoDeHistograma(2,"Equalizacao de Histograma",balloons_matrix)

    # Iniciando a Thread para o Alargamento de Contraste
    thread_alargamento_de_contraste.start()

    # Iniciando a Thread para Equalizacao de Histograma
    thread_equalizacao_de_histograma.start()

    # Esperando que a thread de Alargamento de Contraste seja concluida
    thread_alargamento_de_contraste.join()

    # Esperando que a thread de Equalizacao de Histograma seja concluida
    thread_equalizacao_de_histograma.join()

    # Marca o fim do programa
    fim_do_programa = time.time()

    # Tempos de Execução
    print('-----------------------------------------------------------------')
    print("Tempo de Execução da Thread Alargamento de Contraste: {:.4f}s".format(thread_alargamento_de_contraste._tempo_de_execucao))
    print("Tempo de Execução da Thread Equalização de Histograma: {:.4f}s".format(thread_equalizacao_de_histograma._tempo_de_execucao))
    print("Tempo de Execução do Programa: {:.4f}s".format(fim_do_programa-inicio_do_programa))

    # Exibindo a imagem original e os resultados das threads
    fig = plt.figure(figsize=(15,8))
    # Imagem original
    balloons = fig.add_subplot(2,4,(1,4))
    imgplot = plt.imshow(balloons_img, cmap='gray', vmin=0, vmax=255)
    balloons.set_title("Imagem Original")


    # Alargamento de Contraste
    alargamento_de_contraste = fig.add_subplot(2,4,(5,6))
    imgplot = plt.imshow(thread_alargamento_de_contraste._img_g, cmap='gray', vmin=0, vmax=255)
    alargamento_de_contraste.set_title("Alargamento de Contraste")


    # Equalização de Histograma
    equalizacao_de_histograma = fig.add_subplot(2,4,(7,8))
    imgplot = plt.imshow(thread_equalizacao_de_histograma._img_g, cmap='gray', vmin=0, vmax=255)
    equalizacao_de_histograma.set_title("Equalizacao de Histograma")

    plt.savefig('imagens/resultados.png',bbox_inches='tight')

    # Histogramas
    fig2 = plt.figure(figsize=(15,8))

    balloons_histogram = fig2.add_subplot(2,4,(1,4))
    histplot = plt.hist(balloons_matrix, color=['blue']*640)
    balloons_histogram.set_title("Imagem Original")


    # Alargamento de Contraste
    alargamento_de_contraste_histograma = fig2.add_subplot(2,4,(5,6))
    imgplot = plt.hist(np.array(thread_alargamento_de_contraste._img_g), color=['red']*640)
    alargamento_de_contraste_histograma.set_title("Alargamento de Contraste")


    # Equalização de Histograma
    equalizacao_de_histograma_h = fig2.add_subplot(2,4,(7,8))
    histplot = plt.hist(np.array(thread_equalizacao_de_histograma._img_g), color=['green']*640)
    equalizacao_de_histograma_h.set_title("Equalizacao de Histograma")

    plt.savefig('imagens/histogramas.png',bbox_inches='tight')

    plt.show()
