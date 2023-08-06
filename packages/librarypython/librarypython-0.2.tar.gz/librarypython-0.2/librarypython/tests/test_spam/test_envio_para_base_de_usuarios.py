from unittest.mock import Mock

import pytest

from librarypython.spam.main import EnviadorDeSpam
from librarypython.spam.modelos import Usuario


@pytest.mark.parametrize(
    'usuarios',
    [
        [
            Usuario(nome='Henrique', email='henriquecorreia100@gmail.com'),
            Usuario(nome='Gabriela', email='gabrielafarias20000@gmail.com')
        ],
        [
            Usuario(nome='Henrique', email='henriquecorreia100@gmail.com')
        ]
    ]
)
def test_qtd_de_spam(sessao, usuarios):
    for usuario in usuarios:
        sessao.salvar(usuario)
    # O código abaixo está utilizando a lib Mock
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'henriquecorreia100@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    assert len(usuarios) == enviador.enviar.call_count


def test_parametros_de_spam(sessao):
    usuario = Usuario(nome='Henrique', email='henriquecorreia100@gmail.com')
    sessao.salvar(usuario)
    enviador = Mock()
    enviador_de_spam = EnviadorDeSpam(sessao, enviador)
    enviador_de_spam.enviar_emails(
        'gabrielafarias20000@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
    enviador.enviar.assert_called_once_with(
        'gabrielafarias20000@gmail.com',
        'henriquecorreia100@gmail.com',
        'Curso Python Pro',
        'Confira os módulos fantásticos'
    )
