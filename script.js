document.addEventListener('DOMContentLoaded', () => {
    fetch('/dados')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar dados');
            }
            return response.json();
        })
        .then(data => {
            exibirDados(data);
        })
        .catch(error => {
            console.error(error);
            const dadosContainer = document.getElementById('dados');
            dadosContainer.innerHTML = '<p>Erro ao carregar os dados.</p>';
        });
});

function exibirDados(data) {
    const dadosContainer = document.getElementById('dados');
    dadosContainer.innerHTML = ''; // Limpa qualquer conteúdo anterior

    // Exibe os dados
    for (const cpf in data) {
        const usuario = data[cpf];
        const usuarioDiv = document.createElement('div');
        usuarioDiv.innerHTML = `
            <h3>${usuario.Nome}</h3>
            <p>CPF: ${cpf}</p>
            <p>Saldo: R$ ${usuario.Saldo.toFixed(2)}</p>
            <button onclick="editarUsuario('${cpf}', '${usuario.Nome}', '${usuario.Senha}', '${usuario.SenhaEmergencia}')">Editar</button>
        `;
        dadosContainer.appendChild(usuarioDiv);
    }
}

// Função para editar usuário
function editarUsuario(cpf, nome, senha, senhaEmergencia) {
    document.getElementById('formulario-edicao').style.display = 'block';
    document.getElementById('nome').value = nome;
    document.getElementById('senha').value = senha;
    document.getElementById('senhaEmergencia').value = senhaEmergencia;

    const salvarButton = document.getElementById('salvar');
    salvarButton.onclick = function () {
        const novoNome = document.getElementById('nome').value;
        const novaSenha = document.getElementById('senha').value;
        const novaSenhaEmergencia = document.getElementById('senhaEmergencia').value;

        fetch('/atualizar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cpf: cpf,
                nome: novoNome,
                senha: novaSenha,
                senhaEmergencia: novaSenhaEmergencia,
            }),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao atualizar os dados');
                }
                return response.text();
            })
            .then(mensagem => {
                alert(mensagem);
                document.getElementById('formulario-edicao').style.display = 'none';
                fetch('/dados') // Recarrega os dados
                    .then(response => response.json())
                    .then(data => exibirDados(data));
            })
            .catch(error => {
                console.error(error);
                alert('Erro ao atualizar os dados.');
            });
    };

    const cancelarButton = document.getElementById('cancelar');
    cancelarButton.onclick = function () {
        document.getElementById('formulario-edicao').style.display = 'none';
    };
}

// Função para criar um novo usuário
function criarUsuario() {
    const nome = document.getElementById('novoNome').value;
    const cpf = document.getElementById('novoCPF').value;
    const senha = document.getElementById('novaSenha').value;
    const senhaEmergencia = document.getElementById('novaSenhaEmergencia').value;

    fetch('/criar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            nome: nome,
            cpf: cpf,
            senha: senha,
            senhaEmergencia: senhaEmergencia,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro ao criar o usuário');
        }
        return response.text();
    })
    .then(mensagem => {
        alert(mensagem);
        document.getElementById('novoUsuarioForm').reset(); // Limpa o formulário
        fetch('/dados') // Recarrega os dados
            .then(response => response.json())
            .then(data => exibirDados(data));
    })
    .catch(error => {
        console.error(error);
        alert('Erro ao criar o usuário.');
    });
}

// Adicionando evento ao botão de criar usuário
document.getElementById('criarUsuarioButton').onclick = criarUsuario;

// Adicionando evento ao botão para mostrar/ocultar o formulário de adicionar usuário
document.getElementById('adicionarUsuarioButton').onclick = function() {
    const novoUsuarioDiv = document.getElementById('novo-usuario');
    if (novoUsuarioDiv.style.display === 'none') {
        novoUsuarioDiv.style.display = 'block';
    } else {
        novoUsuarioDiv.style.display = 'none';
    }
};
