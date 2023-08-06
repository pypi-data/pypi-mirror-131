from unittest.mock import Mock

import pytest

from librarypython import librarypythoncodigos


@pytest.fixture
def avatar_url(mocker):
    resp_mock = Mock()
    url = 'https://avatars.githubusercontent.com/u/89937806?v=4'
    resp_mock.json.return_value = {
        'login': 'henriquelima1984', 'id': 89937806,
        'avatar_url': url,
    }
    get_mock = mocker.patch('librarypython.librarypythoncodigos.requests.get')
    get_mock.return_value = resp_mock
    return url


def test_buscar_avatar(avatar_url):
    url = librarypythoncodigos.buscar_avatar('Henriquelima1984')
    assert avatar_url == url


def test_buscar_avatar_integracao():
    url = librarypythoncodigos.buscar_avatar('henriquelima1984')
    assert 'https://avatars.githubusercontent.com/u/89937806?v=4' == url
