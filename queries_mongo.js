// Query 1) Listar todas as modalidades registadas na base de dados:
    db.TesteClinico.find({}, {"atleta.modalidade": true, "_id": false}).pretty()




// Query 2) Listar os atletas registados:
    db.TesteClinico.find({},{"atleta.nome": true, "_id" : false}).pretty()



// Query 3) Listar os atletas e as suas modalidades:
    db.TesteClinico.find({},{"atleta.nome" : 1, "atleta.modalidade" : true, "_id" : false}).pretty()




// Query 4) Listar os nome dos atletas da modalidade: 'salto em altura'
    db.TesteClinico.find({'atleta.modalidade': "Salto em Altura" },{"atleta.nome" : true, "_id" : false}).pretty()



// Query 5) Listar o tipo de testes que se podem realizar na clinica:
    db.TesteClinico.find({},{"tipo": true, "_id" : false}).pretty()



// Query 6) Listar o nome dos atletas que tem testes agendados:
    db.TesteClinico.find({"realizado":false},{"atleta.nome":true ,"_id":false}).pretty()



// Query 7)  Listar o nome dos atletas que foram submetidos a testes clinicos:
    db.TesteClinico.find({"realizado":true},{"atleta.nome":true ,"_id":false}).pretty()



// Query 8) Lista dos dias em o atleta "André sousa figueiredo" tem algum teste clinico marcado:
    db.TesteClinico.find({"atleta.nome" : "André Sousa Figueiredo", "realizado" : false},{"data_hora" : 1,"_id" : 0 }).pretty()



// Query 9) Lista o nome dos profissionais que trabalham na clinica:
    db.TesteClinico.distinct("profissional.nome").pretty()

// Query 10) Número de profissionais que trabalham na clinica:
    db.TesteClinico.distinct("profissional.nome").length


// Query 11) Número de profissionais que ja realizaram pelo menos 1 teste clinico:
    db.TesteClinico.distinct("profissional.nome", {"realizado": true}).length


//Query 12) Atletas cujo o peso se encontra entre 2 paramentros (60Kg E 90Kg) considerado peso saúdavel:
    db.TesteClinico.find({"atleta.peso": {$gt : 60 , $lt:90}}, {"atleta.nome": true, "_id" : false}).pretty()

// View 1
db.TesteClinico.find({"tipo": {$ne : "Controlo Anti-Doping"}, "data_hora": {$gt : new Date(), $lt : new Date(Date.now() + 1000 * 3600 * 24 * 14)}}, {"atleta.nome": true, "tipo": true, "data_hora": true, "_id" : false}).pretty()

// View 2
db.TesteClinico.find({"data_hora": {$gt : new Date(), $lt : new Date(Date.now() + 1000 * 3600 * 24 * 30)}}, {"profissional.nome": true, "data_hora": true, "_id" : false}).pretty()

