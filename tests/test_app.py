import random
import sys
import pytest
from app import create_app
from check_methods import check_status_code_200_get, check_content_text_type_get, check_nonauth_menu_get, \
    check_index_data_get, check_rest_data_get, check_nonexist_rest_get, check_status_code_302_get, \
    check_login_required_get, check_profile_redirection_get, check_auth_menu_get, \
    check_my_profile_auth_data_get, check_foreign_profile_auth_data_get, check_content_image_type_get, \
    check_status_code_200_post, check_status_code_302_post, check_content_text_type_post


def test_config():
    """Test create_app without passing test config"""
    # by default - no test config(False)
    assert not create_app().testing
    # with test config - True
    assert create_app({'TESTING': True}).testing


def test_index(client, auth):
    """Test of index handler: the differences between logged and non-logged in are only in mainmemu"""
    # non logged in
    check_status_code_200_get(client, '/index')
    check_content_text_type_get(client, '/index')
    check_nonauth_menu_get(client, '/index')
    check_index_data_get(client, '/index')

    # logged in
    auth.login()
    check_status_code_200_get(client, '/index')
    check_content_text_type_get(client, '/index')
    check_auth_menu_get(client, '/index')
    check_index_data_get(client, '/index')


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_restaurant(client, auth, rest_id):
    """Test of restaurant handler: the differences between logged and non-logged in are only in mainmemu"""
    # non logged in
    check_status_code_200_get(client, f'/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/restaurant/{rest_id}')
    check_nonauth_menu_get(client, f'/restaurant/{rest_id}')
    check_rest_data_get(client, f'/restaurant/{rest_id}')

    # logged in
    auth.login()
    check_status_code_200_get(client, f'/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/restaurant/{rest_id}')
    check_auth_menu_get(client, f'/restaurant/{rest_id}')
    check_rest_data_get(client, f'/restaurant/{rest_id}')


def test_restaurant_nonexists(client, auth, rest_id=sys.maxsize):
    """Test case when restaurant doesn't exist: returns 404 page not found"""
    # non logged in
    check_status_code_200_get(client, f'/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/restaurant/{rest_id}')
    check_nonexist_rest_get(client, f'/restaurant/{rest_id}')

    # logged in
    auth.login()
    check_status_code_200_get(client, f'/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/restaurant/{rest_id}')
    check_nonexist_rest_get(client, f'/restaurant/{rest_id}')


@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_profile(app, auth, client, username):
    """Test of the profile handler: the differences between logged and non-logged in are redirection to login to see the
    PROFILE page """
    # non logged in
    check_status_code_302_get(client, f'/profile/{username}')
    check_content_text_type_get(client, f'/profile/{username}')
    check_login_required_get(app, client, f'/profile/{username}')

    # logged in( with 'test_name' data!)
    auth.login()
    check_status_code_200_get(client, f'/profile/{username}')
    check_content_text_type_get(client, f'/profile/{username}')
    check_my_profile_auth_data_get(client, f'/profile/test_name')
    check_foreign_profile_auth_data_get(client, f'/profile/test_username')


@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_userava_exists(app, auth, client, username):
    """Test of the user's avatar handler: the differences between logged and non-logged in are redirection to login
     to see the IMAGE"""
    # non logged in
    check_status_code_302_get(client, f'/profile/{username}')
    check_content_text_type_get(client, f'/profile/{username}')
    check_login_required_get(app, client, f'/profile/{username}')

    # logged in
    auth.login()
    check_status_code_200_get(client, f'/userava/{username}')
    check_content_image_type_get(client, f'/userava/{username}')


@pytest.mark.parametrize('url', [f'/profile/{random.random()}', f'/userava/{random.random()}'])
def test_profile_and_userava_nonexists(app, auth, client, url):
    """Test cases when profile and userava don't exist: the differences between logged and non-logged in are redirection
     to login to see the INDEX page """
    # non logged in
    check_status_code_302_get(client, url)
    check_content_text_type_get(client, url)
    check_login_required_get(app, client, url)

    # logged in
    auth.login()
    check_status_code_200_get(client, url)
    check_content_text_type_get(client, url)
    check_auth_menu_get(client, url)
    assert b'div class="flash error"' in client.get(url).data
    check_index_data_get(client, url)


def test_upload(app, client, auth):
    """Test of the upload handler: non logged in -> only GET-request and redirection to login page;
    logged in -> GET-request redirects to profile page; POST-request also redirects to profile page"""
    # non logged in(GET)
    check_status_code_302_get(client, '/upload')
    check_content_text_type_get(client, '/upload')
    check_login_required_get(app, client, '/upload')

    # logged in
    auth.login()
    check_status_code_302_get(client, '/upload')
    check_content_text_type_get(client, '/upload')
    check_content_text_type_post(client, '/upload')
    check_profile_redirection_get(app, client, '/upload')
