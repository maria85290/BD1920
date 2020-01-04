#!/bin/python3
from datetime import datetime, timedelta
from calendar import monthrange

import sys
import os
import random
import numpy.random


primeiros_nomes_genero = {}
consultas = {}


def read_file(filename):
    if not os.path.exists(filename):
        exit(-1)

    with open(filename) as file:
        return [x.strip() for x in file.readlines() if x.strip() != ""]


def gerar_dia(ymin=2019, ymax=2022):
    year = random.randint(ymin, ymax)
    month = random.randint(1, 12)

    return year, month, random.randint(1, monthrange(year, month)[1])


def encontrar_primeira_data_hora_disponivel(year, month, day, hour, minute):
    global consultas

    data_hora = datetime(year, month, day, hour, minute)

    id_medico = 1
    while id_medico in consultas and data_hora.strftime('%Y-%m-%dT%H:%M') in consultas[id_medico]:
        if id_medico < len(consultas):
            id_medico += 1
        else:
            data_hora += timedelta(minutes=15)

            if data_hora.hour >= 18:
                # Depois da hora do fecho, voltamos a abrir às 9:00 do dia seguinte
                data_hora = data_hora.replace(hour=9, minute=0)
                data_hora += timedelta(days=1)

            id_medico = 1
    
    data_hora = data_hora.strftime('%Y-%m-%dT%H:%M')
    if id_medico not in consultas:
        consultas[id_medico] = [data_hora]
    else:
        consultas[id_medico].append(data_hora)

    return id_medico, data_hora


def gerar_sql_modalidades(modalidades):
    for modalidade in modalidades:
        print(f"INSERT INTO Modalidade (nome) VALUES ('{modalidade}');")


def gerar_sql_medicos(medicos):
    for medico in medicos:
        print(f"INSERT INTO Profissional (nome) VALUES ('{medico}');")
        

def gerar_sql_atletas(atletas):
    for nome_atleta in atletas:
        sexo = primeiros_nomes_genero[nome_atleta.split()[0]]
        peso = round(numpy.random.normal(100, 20))
        altura = round(numpy.random.normal(200, 20))
        morada = '{}, Braga'.format(random.choice(freguesias))

        dob = '%d-%d-%d' % gerar_dia(ymin = 1975, ymax = 1995)

        modalidade = random.randint(1, len(modalidades))

        print(f"INSERT INTO Atleta (sexo, nome, peso, altura, morada, DOB, id_modalidade)",
              f"VALUES ('{sexo}', '{nome_atleta}', '{peso}', '{altura}', '{morada}', '{dob}', {modalidade});")


def gerar_sql_provas(modalidades):
    for id_modalidade in range(1, len(modalidades) + 1):
        data_hora = '{}T{}-{}'.format('%d-%d-%d' % gerar_dia(2020, 2022), random.randint(9, 17), random.randint(0, 59))

        duracao = random.randint(1, 2048)

        print(f"INSERT INTO Prova (data_hora, duração, id_modalidade) VALUES ('{data_hora}', {duracao}, {id_modalidade});")


def gerar_sql_testesclinicos_controlodoping(atletas):
    for _ in range(random.randint(1, 60)): # Selecionar o nº de atletas que vão ter testes de controlo anti-doping
        id_atelta_que_realizou = random.randint(1, len(atletas))

        for _ in range(random.randint(1, 3)): # Selecionar quantos testes anti-doping este atleta vai ter
            year, month, day = gerar_dia(2019, 2021)
            hour = random.randint(9, 17)
            minute = random.choice([0, 15, 30, 45])
            id_medico_que_realizou, data_hora = encontrar_primeira_data_hora_disponivel(year, month, day, hour, minute)

            nome = 'Controlo Anti-Doping'
            realizado = random.randint(0, 1) if datetime.fromisoformat(data_hora) < datetime.now() else 0
            preco = random.randint(5, 15)

            print(f"INSERT INTO TesteClinico (nome, realizado, preço, data_hora, id_atleta, id_profissional) VALUES ('{nome}', {realizado}, {preco}, '{data_hora}', {id_atelta_que_realizou}, {id_medico_que_realizou});")

    for j in range(3): # Forçar a que existam pelo menos 1 teste anti-doping nos dias 3, 4 e 5 de janeiro de 2020
        year, month, day = 2020, 1, 3 + j
        hour = random.randint(9, 17)
        minute = random.choice([0, 15, 30, 45])
        id_medico_que_realizou, data_hora = encontrar_primeira_data_hora_disponivel(year, month, day, hour, minute)

        nome = 'Controlo Anti-Doping'
        realizado = random.randint(0, 1) if datetime.fromisoformat(data_hora) < datetime.now() else 0
        preco = random.randint(5, 15) # 5-15 €

        id_atelta_que_realizou = random.randint(1, len(atletas))

        print(f"INSERT INTO TesteClinico (nome, realizado, preço, data_hora, id_atleta, id_profissional) VALUES ('{nome}', {realizado}, {preco}, '{data_hora}', {id_atelta_que_realizou}, {id_medico_que_realizou});")


if __name__ == "__main__":
    random.seed(0)

    atletas = read_file('atletas.txt')
    medicos = read_file('medicos.txt')
    modalidades = read_file('modalidades.txt')
    tipos_testes = read_file('testes.txt')
    freguesias = read_file('freguesias_braga.txt')

    for x in read_file('primeiros_nomes_genero.txt'):
        x = x.strip().split()
        primeiros_nomes_genero[x[0]] = x[1]

    # Selecionar o número de profissionais e de atletas que vamos efetivamente meter na DB
    medicos = [x for x in medicos if random.randint(1, 10) == 1] # Inserir apenas 1/6 dos profissionais
    atletas = [x for x in atletas if random.randint(1, 3) == 1] # Inserir apenas 1/3 dos atletas

    gerar_sql_modalidades(modalidades)
    gerar_sql_medicos(medicos)
    gerar_sql_atletas(atletas)
    gerar_sql_provas(modalidades)
    gerar_sql_testesclinicos_controlodoping(atletas)
