from librarypython.spam.modelos import Usuario


def teste_salvar_usuarios(sessao):
    usuario = Usuario(nome='Henrique', email='henriquecorreia100@gmail.com')
    sessao.salvar(usuario)
    assert isinstance(usuario.id, int)


def teste_listar_usuarios(sessao):
    usuarios = [
        Usuario(nome='Henrique', email='henriquecorreia100@gmail.com'),
        Usuario(nome='Gabriela', email='henriquecorreia100@gmail.com')
    ]
    for usuario in usuarios:
        sessao.salvar(usuario)
    assert usuarios == sessao.listar()
