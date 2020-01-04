-- Configuração necessária para poder apagar certos dados da base de dados
SET SQL_SAFE_UPDATES = 0;

-- View 1) Vista que lista os atletas que têm testes agendados nas próximas duas semanas (excepto testes de controlo Anti-Doping!)
CREATE VIEW Atletas_Testes_Prox2Semanas AS (
	SELECT a.nome AS Atleta,
		   t.nome AS 'Tipo de Teste',
		   t.data_hora as 'Data/Hora'
		FROM Atleta a, TesteClinico t 
		WHERE a.id_atleta = t.id_atleta
			  AND t.data_hora BETWEEN CURRENT_DATE() AND DATE_ADD(CURRENT_DATE(), INTERVAL 14 DAY)
              AND t.nome NOT LIKE '%Controlo Anti-Doping%'
);

-- View 2) Vista que lista todos os profissionais que têm testes marcados durante o próximo mês
CREATE VIEW Profissionais_Testes_ProxMes AS (
	SELECT p.nome AS 'Médico',
		   t.data_hora AS 'Data/Hora'
		FROM Profissional p, TesteClinico t	
		WHERE p.id_profissional = t.id_profissional
			  AND t.data_hora BETWEEN CURRENT_DATE()
              AND DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)
);

-- View 3) Vista que associa a todos os profissionais quais os atletas a quem esse profissional já realizou testes
CREATE VIEW Profissionais_Atletas AS (
	SELECT p.nome AS 'Médico',
		   a.nome AS 'Atleta'
		FROM Profissional p, Atleta a, TesteClinico t
		WHERE t.id_profissional = p.id_profissional
			  AND t.id_atleta = a.id_atleta
		ORDER BY p.nome ASC
);

-- View 4) Vista que associa a cada atleta as provas de atletismo que este vai realizar 
CREATE VIEW Atletas_ProvasAgendadas AS (
	SELECT a.nome AS Atleta,
		   m.nome AS Modalidade,
           p.data_hora AS 'Data/Hora'
		FROM Atleta a, Modalidade m, Prova p
		WHERE m.id_modalidade = a.id_modalidade
              AND m.id_modalidade = p.id_modalidade
);

-- View 5) Vista que associa a cada teste o atleta e o profissional envolvido
CREATE VIEW Teste_Profissional_Atleta AS (
	SELECT a.nome as Atleta,
           t.nome as 'Teste',
           p.nome as 'Médico'
		FROM Atleta a, TesteClinico t, Profissional p
		WHERE t.id_profissional = p.id_profissional
			  AND t.id_atleta = a.id_atleta
		ORDER BY a.nome ASC
);

-- Preparação da Base de Dados para os utilizadores
FLUSH PRIVILEGES;

DELIMITER //
CREATE PROCEDURE Eliminar_Testes_Nao_Realizados()
BEGIN
	DELETE FROM TesteClinico WHERE data_hora < NOW() AND realizado = 0;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE Passar_Teste_a_Realizado(id_prof int, dataHora datetime)
BEGIN
	UPDATE TesteClinico SET realizado = 1 WHERE data_hora = dataHora AND id_prof = id_profissional;
END //
DELIMITER ;

-- Apagar os utilizadores se já existirem
DROP USER IF EXISTS 'atleta'@'localhost';
DROP USER IF EXISTS 'profissional'@'localhost';

-- Criar os utilizadores da base de dados e dar-lhes privilégios
CREATE USER 'atleta'@'localhost' IDENTIFIED BY 'atleta';
GRANT SELECT ON Atletas_Testes_Prox2Semanas TO 'atleta'@'localhost';
GRANT SELECT ON TestesClinicos.Atletas_ProvasAgendadas TO 'atleta'@'localhost';
SHOW GRANTS FOR 'atleta'@'localhost';

CREATE USER 'profissional'@'localhost' IDENTIFIED BY 'prof';
GRANT SELECT ON Profissionais_Testes_ProxMes TO 'profissional'@'localhost';
GRANT EXECUTE ON PROCEDURE Passar_Teste_a_Realizado TO 'profissional'@'localhost';
GRANT INSERT, UPDATE ON TestesClinicos.TesteClinico TO 'profissional'@'localhost';
SHOW GRANTS FOR 'profissional'@'localhost';
