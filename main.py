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


# Realizando a leitura da imagem
balloons_img = Image.open('imagens/balloons.png')

# Obtendo a matriz da imagem
ballonns_matrix = np.array(balloons_img)

balloons_img.show()