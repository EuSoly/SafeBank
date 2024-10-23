const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const porta = 3000;

// Middleware para servir arquivos estáticos
app.use(express.static(path.join(__dirname)));
// Middleware para analisar JSON
app.use(express.json());

// Rota para obter dados do JSON
app.get('/dados', (req, res) => {
    fs.readFile(path.join(__dirname, 'dados.json'), 'utf8', (err, data) => {
        if (err) {
            console.error('Erro ao ler o arquivo JSON:', err);
            res.status(500).send('Erro ao ler o arquivo JSON');
            return;
        }
        res.json(JSON.parse(data));
    });
});

// Rota para atualizar os dados do usuário
app.post('/atualizar', (req, res) => {
    const { cpf, nome, senha, senhaEmergencia } = req.body;
    fs.readFile(path.join(__dirname, 'dados.json'), 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Erro ao ler o arquivo JSON');
            return;
        }
        const usuarios = JSON.parse(data);
        if (usuarios[cpf]) {
            usuarios[cpf].Nome = nome;
            usuarios[cpf].Senha = senha;
            usuarios[cpf].SenhaEmergencia = senhaEmergencia;

            fs.writeFile(path.join(__dirname, 'dados.json'), JSON.stringify(usuarios, null, 4), (err) => {
                if (err) {
                    res.status(500).send('Erro ao atualizar o arquivo JSON');
                    return;
                }
                res.send('Dados atualizados com sucesso!');
            });
        } else {
            res.status(404).send('Usuário não encontrado');
        }
    });
});

// Rota para criar um novo usuário
app.post('/criar', (req, res) => {
    const { nome, cpf, senha, senhaEmergencia } = req.body;
    fs.readFile(path.join(__dirname, 'dados.json'), 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Erro ao ler o arquivo JSON');
            return;
        }
        const usuarios = JSON.parse(data);
        
        // Verifica se o CPF já está cadastrado
        if (usuarios[cpf]) {
            return res.status(400).send('CPF já cadastrado.');
        }
        
        // Adiciona o novo usuário
        usuarios[cpf] = {
            Nome: nome,
            Senha: senha,
            SenhaEmergencia: senhaEmergencia,
            Saldo: 0 // Adicionando saldo padrão
        };

        // Salva as alterações no arquivo JSON
        fs.writeFile(path.join(__dirname, 'dados.json'), JSON.stringify(usuarios, null, 4), (err) => {
            if (err) {
                res.status(500).send('Erro ao salvar o novo usuário no arquivo JSON');
                return;
            }
            res.send('Usuário criado com sucesso!');
        });
    });
});

// Rota padrão
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Inicia o servidor
app.listen(porta, () => {
    console.log(`Servidor rodando em http://localhost:${porta}/`);
});
