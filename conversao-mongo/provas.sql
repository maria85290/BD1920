SELECT p.data_hora, p.duração, m.nome FROM Prova p
INNER JOIN Modalidade m ON p.id_modalidade = m.id_modalidade;