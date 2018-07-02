from plz.util import plz_config
from mock import patch
from io import StringIO
import pytest


@patch('builtins.open')
def test_plz_config_loads_yaml_file(mock_open):
    # Arrange
    test_path = '/test/root/path'
    mock_open.return_value = StringIO("""- id: run
  name: runserver
  cmd: echo "./manage.py runserver"
""")
    expected_result = [{
        "id": "run",
        "name": "runserver",
        "cmd": 'echo "./manage.py runserver"',
    }]

    # Act
    result = plz_config(test_path)

    # Assert
    mock_open.assert_called_with('{}/plz.config'.format(test_path))
    assert(result == expected_result)


def test_plz_config_aborts_if_empty_root():
    # Arrange
    test_path = ''

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config(test_path)


def test_plz_config_aborts_if_null_root():
    # Arrange
    test_path = None

    # Act
    # Assert
    with pytest.raises(Exception):
        plz_config(test_path)


@patch('builtins.open')
def test_plz_config_handles_extra_trailing_slash(mock_open):
    # Arrange
    test_path = '/test/root/path'
    mock_open.return_value = StringIO('')

    # Act
    plz_config(test_path+"/")

    # Assert
    mock_open.assert_called_with('{}/plz.config'.format(test_path))
