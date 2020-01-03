
-- Listar todas as modalidades registadas na base de dados
select nome from Modalidade ;

-- Listar os atletas registados:
select nome from  Atleta;

-- listas os atletas e as suas modalidades.     
select a.nome , m.nome from Atleta a, Modalidade m where a.id_modalidade = m.id_modalidade;

-- listar os nome dos atletas de uma dada modalidade. Por exemplo: 'salto em altura'
 select a.nome, m.nome from Atleta a, Modalidade m 
where a.id_modalidade = m.id_modalidade and m.nome = 'salto em altura';

-- Os testes que se podem realizar:
 select nome from TesteClinico;

-- verificar os testes agendados, retornando o nome dos atletas que tem testes agendados
select a.nome from TesteClinico t, Atleta a
where a.id_atleta = t.id_atleta and t.realizado = 0;
 
-- O nome dos atletas que foram submetidos a testes clinicos e a quantos testes foram submetidos
select distinct a.nome as nome_atleta, (select count(*) from TesteClinico t where a.id_Atleta = t.id_atleta and t.realizado = 1) as numero_Testes_realizados from  Atleta a 
where (select count(*) from TesteClinico t where a.id_Atleta = t.id_atleta and t.realizado = 1)>=1;


-- verificar os dias em que um determinado atleta (por exmplo "LUIS PEDRO BARBOSA FERREIRO") tem algum teste clinico
select distinct (t.data_hora) from Atleta a, TesteClinico t 
where a.nome = 'Luís Pedro Barbosa Ferreira' and a.id_atleta=t.id_atleta and t.realizado = 0;

-- nome dos profissionais que trabalham na clinica
select nome AS Nome from Profissional;

-- numero de profissionais que trabalham na clinica
select distinct count(*) from Profissional;

-- Numero dos profissionais que ja realizaram pelo menos 1 teste clinico
select distinct count(*) as 'Numero de Profissionais' from Profissional p where (
	select count(*) from TesteClinico t where p.id_profissional = t.id_profissional) >= 1;

-- atletas cujo o peso se encontra entre 2 paramentros, considerado peso saudavel. Por exemplo 60 e 80 kg 
select a.nome from Atleta a where (a.peso >= 60) and (a.peso <= 80);

-- associar os atletas aos testes que têm testes agendados nas próximas 2 semanas
CREATE VIEW Atleta_TesteClinico_Prox2semanas AS (
	SELECT a.nome AS Atleta, t.nome AS 'Tipo de Teste', t.data_hora as 'Data/Hora' FROM Atleta a, TesteClinico t 
    WHERE a.id_atleta = t.id_atleta
			and t.data_hora BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 14 DAY) AND t.nome NOT LIKE '%Controlo Anti-Doping%'
	);

-- associar os profissionais aos testes que têm marcados no próximo mês
CREATE VIEW Profissionais_TesteClinico_ProxMes AS (
	SELECT p.nome as Profissional, t.data_hora as 'Dia e hora' FROM Profissional p, TesteClinico t	
    where p.id_profissional = t.id_profissional and t.data_hora BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)
);

-- associar o profissional ao atleta a quem realizaram um teste 
CREATE VIEW Profissionais_Atletas AS (
SELECT p.nome as Profissional, a.nome as 'Atletas consultados' FROM Profissional p, Atleta a, TesteClinico t
where t.id_profissional = p.id_profissional and t.id_atleta = a.id_atleta 
);

-- associar a cada atleta as provas de atletismo que vai realizar 
CREATE VIEW Atletas_ProvasAgendadas AS (
SELECT a.nome as Atleta , m.nome as Modalidade, p.data_hora FROM Atleta a, Modalidade m, Prova p
where m.id_modalidade = a.id_modalidade and m.id_modalidade and m.id_modalidade = p.id_modalidade
);

-- Associar a cada teste_Clinico o atleta e o profissional envolvido

CREATE VIEW Teste_profissional_Atleta AS (
SELECT t.nome as TesteClinico, a.nome as Atleta, p.nome as Profissional FROM Atleta a, TesteClinico t, Profissional p
where t.id_profissional = p.id_profissional and t.id_atleta = a.id_atleta
);


select * from Atleta_TesteClinico_Prox2semanas;
select * from Profissionais_TesteClinico_ProxMes;

create user 'atleta'@'localhost' IDENTIFIED BY 'atl';
GRANT select ON TestesClinicos.atletas_testes To 'atleta'@'localhost';
show grants for 'atleta'@'localhost';

create user 'profissional'@'localhost' IDENTIFIED BY 'prof';
GRANT select ON Profissionais_TesteClinico_ProxMes To 'profissional'@'localhost';
GRANT insert, update on TestesClinicos.TesteClinico To 'profissional'@'localhost';
SHOW GRANTS FOR 'profissional'@'localhost';
