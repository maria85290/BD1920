SELECT tc.nome, tc.realizado, tc.preço, tc.data_hora, atl.nome AS 'nome_atleta', atl.sexo AS 'sexo_atleta', m.nome AS 'modalidade_atleta', atl.peso AS 'peso_atleta', atl.morada as 'morada_atleta', atl.DOB as 'DOB_atleta', prof.nome as 'nome_professional' FROM TesteClinico tc
INNER JOIN Atleta atl ON atl.id_atleta = tc.id_atleta
INNER JOIN Profissional prof ON prof.id_profissional = tc.id_profissional
INNER JOIN Modalidade m ON atl.id_modalidade = m.id_modalidade;