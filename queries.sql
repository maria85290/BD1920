-- Configuração necessária para poder apagar certos dados da base de dados
SET SQL_SAFE_UPDATES = 0;

-- Query 1) Listar todas as modalidades registadas na base de dados
SELECT nome AS 'Atleta'
	FROM Modalidade;

-- Query 2) Listar os atletas registados
SELECT nome as 'Atleta'
	FROM  Atleta;

-- Query 3) Listar os atletas e as suas modalidades
SELECT a.nome AS 'Atleta', m.nome AS 'Modalidade'
	FROM Atleta a, Modalidade m
    WHERE a.id_modalidade = m.id_modalidade;

-- Query 4) Listar os nome dos atletas de uma dada modalidade, por exemplo: 'Salto em Altura'
SELECT a.nome AS 'Atleta', m.nome AS 'Modalidade'
	FROM Atleta a, Modalidade m 
	WHERE a.id_modalidade = m.id_modalidade
		  AND m.nome = 'Salto em Altura';

-- Query 5) Listar o tipo de testes que já foram realizados
SELECT nome AS 'Tipo de Teste'
	FROM TesteClinico
	GROUP BY nome;

-- Query 6) Verificar os testes agendados, retornando o nome dos atletas que tem testes agendados
SELECT a.nome AS 'Atleta'
	FROM TesteClinico t, Atleta a
	WHERE a.id_atleta = t.id_atleta
		  AND t.realizado = 0
	GROUP BY a.nome;
 
-- Query 7) O nome dos atletas que foram submetidos a testes clinicos e a quantos testes foram submetidos
SELECT DISTINCT a.nome as 'Atleta',
				(SELECT COUNT(*) FROM TesteClinico t WHERE a.id_Atleta = t.id_atleta AND t.realizado = 1) AS 'Número de Testes Realizados'
	FROM  Atleta a 
	WHERE (SELECT COUNT(*) FROM TesteClinico t WHERE a.id_Atleta = t.id_atleta AND t.realizado = 1) >= 1;


-- Query 8) Verificar os dias em que um determinado atleta (por exmplo "LUIS PEDRO BARBOSA FERREIRO") tem algum teste clinico
SELECT DISTINCT t.data_hora AS 'Data/Hora'
	FROM Atleta a, TesteClinico t 
	WHERE a.nome = 'Luís Pedro Barbosa Ferreira'
		  AND a.id_atleta = t.id_atleta
		  AND t.realizado = 0;

-- Query 9) Nome dos profissionais que trabalham na clínica
SELECT nome AS 'Médico'
	FROM Profissional;

-- Query 10) Número de profissionais que trabalham na clínica
SELECT DISTINCT COUNT(*)
	FROM Profissional;

-- Query 11) Número dos profissionais que já realizaram pelo menos 1 teste clínico
SELECT DISTINCT COUNT(*) AS 'Número de Profissionais'
	FROM Profissional p
    WHERE (SELECT COUNT(*) FROM TesteClinico t WHERE p.id_profissional = t.id_profissional) >= 1;

-- Query 12) Atletas cujo o peso se encontra dentro de um intervalo (i.e., têm um peso saudável). Por exemplo 60 e 90 kg 
SELECT a.nome
	FROM Atleta a
	WHERE a.peso >= 60
		  AND a.peso <= 90;
