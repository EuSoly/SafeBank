document.getElementById('create-account-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const nome = document.getElementById('nome').value;
    const cpf = document.getElementById('cpf').value;
    const senha = document.getElementById('senha').value;
    const senhaEmergencia = document.getElementById('senha-emergencia').value;

    const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};

    if (usuarios[cpf]) {
        document.getElementById('message').innerText = 'CPF já cadastrado.';
        return;
    }

    usuarios[cpf] = {
        Nome: nome,
        Senha: senha,
        SenhaEmergencia: senhaEmergencia,
        Saldo: 0.0
    };
    
    localStorage.setItem('usuarios', JSON.stringify(usuarios));
    alert('Conta criada com sucesso!');
    window.location.href = 'login.html';
});

document.getElementById('login-form')?.addEventListener('submit', function(event) {
    event.preventDefault();

    const cpf = document.getElementById('cpf-login').value;
    const senha = document.getElementById('senha-login').value;

    const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};

    if (!usuarios[cpf]) {
        document.getElementById('message').innerText = 'CPF não encontrado.';
        return;
    }

    if (usuarios[cpf].Senha === senha) {
        localStorage.setItem('loggedUser', cpf);
        window.location.href = 'dashboard.html';
    } else {
        document.getElementById('message').innerText = 'Senha incorreta.';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const loggedUser = localStorage.getItem('loggedUser');
    if (loggedUser) {
        const usuarios = JSON.parse(localStorage.getItem('usuarios'));
        document.getElementById('user-info').innerText = `Olá, ${usuarios[loggedUser].Nome}! Seu saldo é R$ ${usuarios[loggedUser].Saldo.toFixed(2)}`;
    }

    document.getElementById('logout-button')?.addEventListener('click', function() {
        localStorage.removeItem('loggedUser');
        window.location.href = 'login.html';
    });

    // Lógica de depósito
    document.getElementById('confirm-deposito')?.addEventListener('click', function() {
        const valor = parseFloat(document.getElementById('valor-deposito').value);
        const usuarios = JSON.parse(localStorage.getItem('usuarios'));

        if (!isNaN(valor) && valor > 0) {
            usuarios[loggedUser].Saldo += valor;
            localStorage.setItem('usuarios', JSON.stringify(usuarios));
            alert(`Depósito de R$ ${valor.toFixed(2)} realizado com sucesso!`);
            window.location.href = 'dashboard.html'; 
        } else {
            alert("Valor inválido.");
        }
    });

    // Lógica de saque
    document.getElementById('confirm-saque')?.addEventListener('click', function() {
        const valor = parseFloat(document.getElementById('valor-saque').value);
        const usuarios = JSON.parse(localStorage.getItem('usuarios'));

        if (!isNaN(valor) && valor > 0) {
            if (usuarios[loggedUser].Saldo >= valor) {
                usuarios[loggedUser].Saldo -= valor;
                localStorage.setItem('usuarios', JSON.stringify(usuarios));
                alert(`Saque de R$ ${valor.toFixed(2)} realizado com sucesso!`);
                window.location.href = 'dashboard.html'; 
            } else {
                alert("Saldo insuficiente.");
            }
        } else {
            alert("Valor inválido.");
        }
    });

    // Lógica de transferência
    document.getElementById('confirm-transferencia')?.addEventListener('click', function() {
        const destinatario = document.getElementById('cpf-destinatario').value;
        const valor = parseFloat(document.getElementById('valor-transferencia').value);
        const usuarios = JSON.parse(localStorage.getItem('usuarios'));

        if (usuarios[destinatario]) {
            if (!isNaN(valor) && valor > 0) {
                if (usuarios[loggedUser].Saldo >= valor) {
                    usuarios[loggedUser].Saldo -= valor;
                    usuarios[destinatario].Saldo += valor;
                    localStorage.setItem('usuarios', JSON.stringify(usuarios));
                    alert(`Transferência de R$ ${valor.toFixed(2)} para ${usuarios[destinatario].Nome} realizada com sucesso!`);
                    window.location.href = 'dashboard.html'; 
                } else {
                    alert("Saldo insuficiente.");
                }
            } else {
                alert("Valor inválido.");
            }
        } else {
            alert("Destinatário não encontrado.");
        }
    });
});
