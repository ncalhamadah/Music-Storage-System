import os
from unittest import mock
from unittest.mock import MagicMock

from sqlmodel import Session
from typer.testing import CliRunner

from main import app
from models.role import Role
from models.user import User
from src.utils.configLoader import ConfigLoader
from utils.schema.token_input import TokenInput


# @mock.patch("src.main.ConfigLoader.load_config")
# def test_list_music_data(
#         mock__ConfigLoader__load_config
# ):
#     mock__ConfigLoader__load_config.return_value = None
#     runner = CliRunner()
#     result = runner.invoke(cli, ['list-music-data'])
#     assert 'listing' in result.output

def side_effect(arg):
    test = MagicMock(ConfigLoader())
    test.load_config.return_value = "YOL"
    values = {'config_loader': test, 'b': 2, 'c': 3}
    return values[arg]


@mock.patch("src.main.ConfigFactory.create_object")
def test_when_list_music_data_then_is_listed(
        mock__creator
):
    test = MagicMock(ConfigLoader())

    test.load_config.return_value = MagicMock(Session)
    mock__creator.side_effect = side_effect
    runner = CliRunner()
    result = runner.invoke(app, ['list-music-data'], input="hello\nworld")
    assert 'hello' in result.output


@mock.patch("src.main.LoginController.login")
def test_when_login_with_right_credentials_then_user_is_logged_on(
        mock_login
):
    # test = MagicMock(ConfigLoader())
    #
    mock_login.return_value = TokenInput(user_data=User(), role=Role())
    runner = CliRunner()
    result = runner.invoke(app, ['login'], input="hello\nworld")
    assert mock_login.call_count == 1
    assert 'logged_in' in result.output


@mock.patch("src.main.ConfigFactory.create_object")
def test_when_delete_music_data_with_right_credentials_then_music_data_is_deleted(
        mock__creator
):
    test = MagicMock(ConfigLoader())

    test.load_config.return_value = "YOL"
    mock__creator.side_effect = side_effect
    runner = CliRunner()
    result = runner.invoke(app, ['delete-music-data'])
    assert 'deleting' in result.output

@mock.patch("src.main.LoginController.add_new_user")
@mock.patch("src.main.LoginController.login")
def test_when_add_new_user_as_a_admin_then_user_is_created(
        mock_login, mock_add_new_user
):
    test = MagicMock(ConfigLoader())

    test.load_config.return_value = "YOL"
    mock_login.return_value = TokenInput(user_data=User(), role=Role(role_name="ADMIN"))
    # mock__creator.side_effect = side_effect
    runner = CliRunner()
    result = runner.invoke(app, ['add-new-user-and-role'], input="hello\nworld\ntest_user\ntest_pass\ntest_pass\nADMIN")
    assert 'test_user' in result.output


@mock.patch.object(os.environ, "get")
@mock.patch("src.main.LoginController.login")
def test_when_add_new_user_as_a_normal_user_then_access_denied(
        mock_login, mock_os
):
    test = MagicMock(ConfigLoader())
    mock_os.return_value = ""
    test.load_config.return_value = "YOL"
    mock_login.return_value = TokenInput(user_data=User(), role=Role(role_name="SOME_ROLE"))
    # mock__creator.side_effect = side_effect
    runner = CliRunner()
    result = runner.invoke(app, ['add-new-user-and-role'], input="hello\nworld\ntester\ntest_pass\ntest_pass\nNORMAL_USER")
    assert 'access_denied' in result.output
