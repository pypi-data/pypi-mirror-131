import pytest

from librarypython.spam.enviador_de_email import Enviador, EmailInvalido


def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None


@pytest.mark.parametrize(
    'destinatario',
    ['foo@bar.com.br', 'henriquecorreia100@gmail.com']
)
def test_remetente(destinatario):
    enviador = Enviador()

    resultado = enviador.enviar(
        destinatario,
        'gabrielafarias20000@gmail.com',
        'Curso Python Pro',
        'Turma Henrique Correia aberta.'
    )
    assert destinatario in resultado


@pytest.mark.parametrize(
    'remetente',
    ['', 'henrique']
)
def test_remetente_(remetente):
    enviador = Enviador()
    with pytest.raises(EmailInvalido):
        enviador.enviar(
            remetente,
            'gabrielafarias20000@gmail.com',
            'Curso Python Pro',
            'Turma Henrique Correia aberta.'
        )
