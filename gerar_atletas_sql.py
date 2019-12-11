#!/bin/python3
import sys
import os
import random
import numpy.random


def read_file(filename):
    if not os.path.exists(filename):
        exit(-1)

    with open(filename) as file:
        return file.readlines()


if __name__ == "__main__":
    atletas = read_file('atletas.txt')
    medicos = read_file('medicos.txt')
    modalidades = read_file('modalidades.txt')
    tipos_testes = read_file('testes.txt')

    random.seed(0)

    # Cada atleta tem:
    ## id
    ## sexo
    ## nome
    ## peso
    ## altura
    ## morada
    ## date of birth
    ## modalidade que pratica
    for nome_alteta in atletas:
        sexo = random.choice(['M', 'F'])
        peso = random.choice()