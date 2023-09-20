import pytest
from tests.check_methods import check_status_code_302_get, check_content_text_type_get, check_profile_redirection_get, \
    check_status_code_200_get, check_registration_data_get, check_registration_data_post, check_status_code_302_post, \
    check_content_text_type_post, check_status_code_200_post, check_validate_register, check_login_data_get, \
    check_login_data_post, check_validate_login, check_logout_data_get


# messages = errors
@pytest.mark.parametrize(('username', 'email', 'password', 'password2', 'message'), (
        ('', 'aaaaa@gmail.com', '47595340', '47595340', b'Username is required'),
        ('a', 'aaaaa@gmail.com', '47595340', '47595340', b'Name length should be from 4 to 100 symbols'),
        ('aaaa', 'aaaaa', '47595340', '47595340', b'Invalid email'),
        ('aaaa', 'aaaaa@gmail.com', '', '', b'Password is required'),
        ('aaaa', 'aaaaa@gmail.com', '12', '12', b'Password length should be from 4 to 100 symbols'),
        ('aaaa', 'aaaaa@gmail.com', '47595340', '47340', b"Passwords dont match"),
))
def test_register(client, app, auth, username, email, password, password2, message, url='/register'):
    """Test of register handler:
    - non logged in can do GET -> redirects to registration page - or POST -> registrates and redirects to login page;
    - logged in can do only GET -> redirects to profile page"""

    # non logged in - BEFORE LOGIN
    check_status_code_200_get(client, url)
    check_content_text_type_get(client, url)
    check_registration_data_get(client, url)
    check_registration_data_post(app, client, url)
    # test different invalid input and error messages
    check_validate_register(client, url, username, email, password, password2, message)

    # logged in
    auth.login()
    check_status_code_302_get(client, url)
    check_content_text_type_get(client, url)
    check_profile_redirection_get(app, client, url)


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('a', 'test', b'Incorrect username.'),
        ('test_name', 'a', b'Incorrect password.'),
))
def test_login(client, auth, app, username, password, message, url='/login'):
    """Test of login handler:
        - non logged in can do GET -> redirects to login page - or POST -> logs in and redirects to profile or another wanted page;
        - logged in can do only GET -> redirects to profile page"""

    # non logged in - BEFORE LOGIN
    check_status_code_200_get(client, url)
    check_content_text_type_get(client, url)
    check_login_data_get(client, url)
    check_validate_login(auth, username, password, message)

    # does log in also!
    check_login_data_post(client, auth)
    # already logged in
    check_status_code_302_get(client, url)
    check_content_text_type_get(client, url)
    check_profile_redirection_get(app, client, url)


def test_logout(client, auth, url='/logout'):
    auth.login()
    # logged in and the logged out
    check_logout_data_get(auth, client, url)
