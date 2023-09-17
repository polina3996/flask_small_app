import random
import sys
import pytest
from app import create_app
from check_methods import check_status_code_200_get, check_content_text_type_get, check_nonauth_menu_get, \
    check_index_data_get, check_rest_data_get, check_nonexist_rest_get, check_status_code_302_get, \
    check_login_required_get, check_profile_redirection_get


def test_config():
    """Test create_app without passing test config"""
    # by default - no test config(False)
    assert not create_app().testing
    # with test config - True
    assert create_app({'TESTING': True}).testing


def test_index(client, auth):
    """Test of main page: the differences between logged and non-logged in are only in mainmemu"""
    # non logged in
    check_status_code_200_get(client, '/index')
    check_content_text_type_get(client, '/index')
    check_nonauth_menu_get(client, '/index')
    check_index_data_get(client)

    # logged in
    # auth.login()
    # check_status_code_200_get(client, '/index')
    # check_content_text_type_get(client, '/index')
    # check_auth_menu_get(client, '/index')
    # check_index_data_get(client)


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_restaurant(client, rest_id):
    """Test of any of restaurant pages: the differences between logged and non-logged in are only in mainmemu"""
    # non logged in
    check_status_code_200_get(client, f'/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/restaurant/{rest_id}')
    check_nonauth_menu_get(client, f'/restaurant/{rest_id}')
    check_rest_data_get(client, f'/restaurant/{rest_id}')

    # logged in
    # auth.login()
    # check_status_code_200_get(client, f'/restaurant/{rest_id}')
    # check_content_text_type_get(client, f'/restaurant/{rest_id}')
    # check_auth_menu_get(client, f'/restaurant/{rest_id}')
    # check_rest_data_get(client, f'/restaurant/{rest_id}')


def test_restaurant_nonexists(client, rest_id=sys.maxsize):
    """Test of the page when restaurant doesn't exist: returns 404 page not found"""
    check_status_code_200_get(client, f'/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/restaurant/{rest_id}')
    check_nonexist_rest_get(client, f'/restaurant/{rest_id}')


@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_profile(app, client, username):
    """Test of the profile page: the differences between logged and non-logged in are redirection to login to see the
    PROFILE page """
    # non logged in
    check_status_code_302_get(client, f'/profile/{username}')
    check_content_text_type_get(client, f'/profile/{username}')
    check_login_required_get(app, client, f'/profile/{username}')

    # logged in
    # auth.login()
    # check_status_code_200_get(client, f'/profile/{username}')
    # check_content_text_type_get(client, f'/profile/{username}')
    # check_profile_auth_data_get(client, f'/profile/{username}')


@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_userava_exists(app, client, username):
    # non logged in
    check_status_code_302_get(client, f'/profile/{username}')
    check_content_text_type_get(client, f'/profile/{username}')
    check_login_required_get(app, client, f'/profile/{username}')

    # logged in
    # auth.login()
    # check_status_code_200_get(client, f'/userava/{username}')
    # check_content_image_type_get(client, f'/userava/{username}')


def test_profile_and_userava_nonexists(app, client, username=random.random()):
    """Test of the profile and userava pages that don't exist: the differences between logged and non-logged in are redirection to
    login to see the INDEX page """
    # non logged in
    check_status_code_302_get(client, f'/profile/{username}')
    check_content_text_type_get(client, f'/profile/{username}')
    check_login_required_get(app, client, f'/profile/{username}')

    # logged in
    # auth.login()
    # check_status_code_200_get(client, f'/profile/{username}')
    # check_content_text_type_get(client, f'/profile/{username}')
    # check_auth_menu_get(client, '/index')
    # check_index_data_get(client)


def test_upload(app, client):
    """Test of the uploading of the user's avatar method: non logged in -> only GET-request and redirection to login page;
    logged in -> GET-request redirects to profile page; POST-request also redirects to profile page"""
    # non logged in(GET)
    check_status_code_302_get(client, f'/upload')
    check_content_text_type_get(client, f'/upload')
    check_login_required_get(app, client, f'/upload')

    # logged in(GET)
    # auth.login()
    # check_status_code_302_get(client, f'/upload')
    # check_content_text_type_get(client, f'/upload')
    # check_profile_redirection_get(app, client, f'/upload')

    # logged in(POST)
    # auth.login()
    # check_status_code_302_post(client, f'/upload')
    # check_content_text_type_post(client, f'/upload')
    # check_profile_redirection_post(app, client, f'/upload')
