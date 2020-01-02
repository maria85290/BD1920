-- Listar todas as modalidades registadas na base de dados

select nome from Modalidade ;


-- Listar os atletas registados:

select nome from  Atleta;



-- listas os atletas e as suas modalidades. 
    
select a.nome , m.nome from atleta a, modalidade m where a.id_modalidade = m.id_modalidade;




-- listar os nome dos atletas de uma dada modalidade. Por exemplo: 'salto em altura'

 select a.nome, m.nome from atleta a, modalidade m 
where a.id_modalidade = m.id_modalidade and m.nome = 'salto em altura' 




-- Os testes que se podem realizar:
   
 select nome from testesclinicos 




-_ verificar os testes agendados, retornando o nome dos atletas que tem testes agendados
	 
select t.nome, a.nome from testesclinicos t , atleta a
where a.id_atleta in (select c.id_atleta from atleta_testes_clinicos c , testesclinicos t 
                               where c.id_teste_clinico = t.id_teste_clinico and t.realizado = 0)
 


-- O nome dos atletas que foram submetidos a testes clinicos

	 select distinct a.nome from  atleta a, testesclinicos t where
            a.id_atleta in (select c.id_atleta from atleta_testes_clinicos c , testesclinicos t 
                               where c.id_teste_clinico = t.id_teste_clinico and t.realizado = 1)



-- O testes clinicos que os atletas de uma determinada modalidade

select distinct t.nome from testesclinicos t where t.id_teste_clinico in 
(select c.id_teste_clinico from atleta_testes_clinicos c where c.id_atleta 
in ( select id_atleta from atleta where id_modalidade
in ( select m.id_modalidade from modalidade m where m.nome = 'Lançamento do Dardo' )))   


-- verificar os dias em que um determinado atleta (por exmplo "LUIS PEDRO BARBOSA FERREIRO") tem algum teste clinico

select distinct (c.data_hora) from Atleta a, testesclinicos c 
where a.nome = 'Luís Pedro Barbosa Ferreira' and a.id_atleta in (select c.id_atleta from atleta_testes_clinicos c , testesclinicos t 
where c.id_teste_clinico = t.id_teste_clinico and t.realizado = 0)


-- verificar se ocorre subreposiçao de horarios das provas com horarios da realizaçao de testes clinicos. No caso de ser retornado algum 
-- nome de atleta significa que existe uma prova desse atleta subposta com a realizaçao de um exame 

select a.nome from atleta  a where a.id_atleta in (select c.id_atleta from atleta_testes_clinicos c where c.id_teste_clinico 
in ( select t.id_teste_clinico from testesclinicos t where t.data_hora in (select p.data_hora from prova p)))

-- nome dos profissionais que trabalham na clinica
select nome AS Nome from profissional

-- numero de profissionais que trabalham na clinica
select distinct count(nome) from profissional;


-- Numero dos profissionais que ja realizaram pelo menos 1 teste clinico
select distinct count(p.nome) from profissional p where p.id_profissional in (select id_profissional from teste_profissional);

-- atletas cujo o peso se encontra entre 2 paramentros, considerado peso saudavel. Por exemplo 60 e 80 kg 
select a.nome from atleta a where (a.peso >= 60) and (a.peso <= 80);

-- consultar os testes agendados

-- associar os atletas aos testes que têm agendados
create view atletas_testes as
	select atl.nome as nome_atleta, tc.nome as teste_clinico, tc.data_hora as dia_hora from Atleta atl, TesteClinico tc, Atleta_Teste_Clinico atc
    where atl.id_atleta = atc.id_atleta and atc.id_teste_clinico = tc.id_teste_clinico;

create user 'atleta'@'localhost' IDENTIFIED BY 'atl';

GRANT select ON TestesClinicos.atletas_testes To 'atleta'@'localhost';
-- REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'atleta'@'localhost';
flush privileges;

show grants for 'atleta'@'localhost';
