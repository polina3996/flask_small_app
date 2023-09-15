import sys
import pytest
from app import create_app
from check_methods import check_status_code, check_content_type, check_nonauth_menu, check_auth_menu, check_index_data, \
    check_rest_data, check_nonexist_rest


def test_config():
    """Test create_app without passing test config"""
    # by default - no test config(False)
    assert not create_app().testing
    # with test config - True
    assert create_app({'TESTING': True}).testing


def test_index(client, auth):
    """Test of main page"""
    # non logged in
    check_status_code(client, '/index')
    check_content_type(client, '/index')
    check_nonauth_menu(client, '/index')
    check_index_data(client)

    # logged in
    # auth.login()
    # check_status_code(client, '/index')
    # check_content_type(client, '/index')
    # check_auth_menu(client, '/index')
    # check_index_data(client)


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_restaurant(client, rest_id):
    """Test of any of restaurant pages"""
    # non logged in
    check_status_code(client, f'/restaurant/{rest_id}')
    check_content_type(client, f'/restaurant/{rest_id}')
    check_nonauth_menu(client, f'/restaurant/{rest_id}')
    check_rest_data(client, f'/restaurant/{rest_id}')

    # logged in
    # auth.login()
    # check_status_code(client, f'/restaurant/{rest_id}')
    # check_content_type(client, f'/restaurant/{rest_id}')
    # check_auth_menu(client, f'/restaurant/{rest_id}')
    # check_rest_data(client, f'/restaurant/{rest_id}')


def test_restaurant_nonexist(client, rest_id=sys.maxsize):
    """Test of the 404 page when restaurant doesn't exist"""
    check_status_code(client, f'/restaurant/{rest_id}')
    check_content_type(client, f'/restaurant/{rest_id}')
    check_nonexist_rest(client, f'/restaurant/{rest_id}')


@pytest.mark.parametrize('username', [])
def test_profile(client, username):
    """Test of the profile page"""
    response = client.get(f'/profile/{username}')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert b'html' in response.data
    assert b'p class="none"' in response.data




#assert b'' in response.data