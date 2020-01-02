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
	 
select t.nome, a.nome from TestesClinicos t , Atleta a
where a.id_atleta in (select c.id_atleta from Atleta_TesteClinico c , TesteClinico t 
                               where c.id_testeclinico = t.id_testeclinico and t.realizado = 0);
 


-- O nome dos atletas que foram submetidos a testes clinicos

	 select distinct a.nome from  Atleta a, TesteClinico t where
            a.id_atleta in (select c.id_atleta from Atleta_TesteClinico c , TesteClinico t 
                               where c.id_testeclinico = t.id_testeclinico and t.realizado = 1);



-- O testes clinicos que os atletas de uma determinada modalidade

select distinct t.nome from TesteClinico t where t.id_testeclinico in 
(select c.id_testeclinico from Atleta_TesteClinico c where c.id_atleta 
in ( select id_atleta from atleta where id_modalidade
in ( select m.id_modalidade from Modalidade m where m.nome = 'Lançamento do Dardo' ))); 


-- verificar os dias em que um determinado atleta (por exmplo "LUIS PEDRO BARBOSA FERREIRO") tem algum teste clinico

select distinct (c.data_hora) from Atleta a, TesteClinico c 
where a.nome = 'Luís Pedro Barbosa Ferreira' and a.id_atleta in (select c.id_atleta from Atleta_testeClinico c , TesteClinico t 
where c.id_testeclinico = t.id_testeclinico and t.realizado = 0);


-- verificar se ocorre subreposiçao de horarios das provas com horarios da realizaçao de testes clinicos. No caso de ser retornado algum 
-- nome de atleta significa que existe uma prova desse atleta subposta com a realizaçao de um exame 

select a.nome from atleta  a where a.id_atleta in (select c.id_atleta from Atleta_testeClinico c where c.id_testeclinico 
in ( select t.id_testeclinico from TesteClinico t where t.data_hora in (select p.data_hora from prova p)));

-- nome dos profissionais que trabalham na clinica
select nome AS Nome from profissional;

-- numero de profissionais que trabalham na clinica
select distinct count(nome) from profissional;


-- Numero dos profissionais que ja realizaram pelo menos 1 teste clinico
select distinct count(p.nome) from Profissional p where p.id_profissional in (select id_profissional from TesteClinico_Profissional);

-- atletas cujo o peso se encontra entre 2 paramentros, considerado peso saudavel. Por exemplo 60 e 80 kg 
select a.nome from Atleta a where (a.peso >= 60) and (a.peso <= 80);

-- associar os atletas aos testes que têm testes agendados nas próximas 2 semanas
CREATE VIEW Atleta_TesteClinico_Prox2Semanas AS (
	SELECT nome AS Atleta, t.nome AS 'Tipo de Teste', t.data_hora as 'Data/Hora' FROM Atleta WHERE id_atleta IN (
		SELECT id_atleta FROM Atleta_TesteClinico WHERE id_testeclinico IN (
			SELECT id_testeclinico FROM TesteClinico t WHERE data_hora BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 14 DAY) AND nome NOT LIKE '%Controlo Anti-Doping%'
		)
	)
);

-- associar os profissionais aos testes que têm marcados no próximo mês
CREATE VIEW Profissionais_TesteClinico_ProxMes AS (
	SELECT nome AS Profissional FROM Profissional WHERE id_profissional IN (
		SELECT id_profissional FROM TesteClinico_Profissional WHERE id_testeclinico IN (
			SELECT id_testeclinico FROM TesteClinico WHERE data_hora BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)
		)
	)
);

select * from profissionais_testes;

create user 'atleta'@'localhost' IDENTIFIED BY 'atl';

GRANT select ON TestesClinicos.atletas_testes To 'atleta'@'localhost';
-- REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'atleta'@'localhost';
flush privileges;

show grants for 'atleta'@'localhost';

create user 'profissional'@'localhost' IDENTIFIED BY 'prof';

GRANT select ON TestesClinicos.atletas_testes To 'atleta'@'localhost';


DELIMITER //
CREATE TRIGGER `ATLETA_INSERIR_TESTESPERIODICOS`
AFTER INSERT
ON Atleta
FOR EACH ROW
BEGIN
	# INSERT INTO 
END; //
DELIMITER ;

select * from mysql.user;