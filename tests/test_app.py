import random
import sys
import pytest
from flask import make_response
from app import create_app
from check_methods import check_status_code_200, check_status_code_302, check_content_text_type, \
    check_content_image_type, check_nonauth_menu, \
    check_auth_menu, check_index_data, \
    check_rest_data, check_nonexist_rest, \
    check_profile_auth_data, check_login_required


def test_config():
    """Test create_app without passing test config"""
    # by default - no test config(False)
    assert not create_app().testing
    # with test config - True
    assert create_app({'TESTING': True}).testing


def test_index(client, auth):
    """Test of main page: the differences between logged and non-logged in are only in mainmemu"""
    # non logged in
    check_status_code_200(client, '/index')
    check_content_text_type(client, '/index')
    check_nonauth_menu(client, '/index')
    check_index_data(client)

    # logged in
    # auth.login()
    # check_status_code_200(client, '/index')
    # check_content_text_type(client, '/index')
    # check_auth_menu(client, '/index')
    # check_index_data(client)


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_restaurant(client, rest_id):
    """Test of any of restaurant pages: the differences between logged and non-logged in are only in mainmemu"""
    # non logged in
    check_status_code_200(client, f'/restaurant/{rest_id}')
    check_content_text_type(client, f'/restaurant/{rest_id}')
    check_nonauth_menu(client, f'/restaurant/{rest_id}')
    check_rest_data(client, f'/restaurant/{rest_id}')

    # logged in
    # auth.login()
    # check_status_code_200(client, f'/restaurant/{rest_id}')
    # check_content_text_type(client, f'/restaurant/{rest_id}')
    # check_auth_menu(client, f'/restaurant/{rest_id}')
    # check_rest_data(client, f'/restaurant/{rest_id}')


def test_restaurant_nonexists(client, rest_id=sys.maxsize):
    """Test of the page when restaurant doesn't exist: returns 404 page not found"""
    check_status_code_200(client, f'/restaurant/{rest_id}')
    check_content_text_type(client, f'/restaurant/{rest_id}')
    check_nonexist_rest(client, f'/restaurant/{rest_id}')


@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_profile(app, client, username):
    """Test of the profile page: the differences between logged and non-logged in are redirection to login to see the
    PROFILE page """
    # non logged in
    check_status_code_302(client, f'/profile/{username}')
    check_content_text_type(client, f'/profile/{username}')
    check_login_required(app, client, f'/profile/{username}')

    # logged in
    # check_status_code_200(client, f'/profile/{username}')
    # check_content_text_type(client, f'/profile/{username}')
    # check_profile_auth_data(client, f'/profile/{username}')

    
@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_userava_exists(app, client, username):
    # non logged in
    check_status_code_302(client, f'/profile/{username}')
    check_content_text_type(client, f'/profile/{username}')
    check_login_required(app, client, f'/profile/{username}')

    # logged in
    # check_status_code_200(client, f'/userava/{username}')
    # check_content_image_type(client, f'/userava/{username}')


def test_profile_and_userava_nonexists(app, client, username=random.random()):
    """Test of the profile and userava pages that don't exist: the differences between logged and non-logged in are redirection to
    login to see the INDEX page """
    # non logged in
    check_status_code_302(client, f'/profile/{username}')
    check_content_text_type(client, f'/profile/{username}')
    check_login_required(app, client, f'/profile/{username}')

    # logged in
    # check_status_code_200(client, f'/profile/{username}')
    # check_content_text_type(client, f'/profile/{username}')
    # check_auth_menu(client, '/index')
    # check_index_data(client)





