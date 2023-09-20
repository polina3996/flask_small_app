from flask import make_response, session, g
from db import get_db
from FDataBase import FDataBase


def check_status_code_200_get(client, url):
    # GET-request and returning a Response object
    response = client.get(url)
    assert response.status_code == 200


def check_status_code_200_post(client, url):
    # POST-request, converting the *data-dictionary into form-data
    response = client.post(url)
    assert response.status_code == 200


def check_status_code_302_get(client, url):
    response = client.get(url)
    assert response.status_code == 302


def check_status_code_302_post(client, url):
    response = client.post(url)
    assert response.status_code == 302


def check_content_text_type_get(client, url):
    response = client.get(url)
    assert response.content_type == 'text/html; charset=utf-8'


def check_content_text_type_post(client, url):
    response = client.post(url)
    assert response.content_type == 'text/html; charset=utf-8'


def check_content_image_type_get(client, url):
    response = client.get(url)
    assert response.content_type == 'image/png'


def check_404_get(client, url):
    response = client.get(url)
    assert b'html' in response.data
    assert b'p class="none"' in response.data


def check_login_required_get(app, client, url):
    # creating the app context
    with app.app_context():
        response = client.get(url)
        # converting to response object
        resp = make_response(response)
        # redirects to login page
        assert '/login' in resp.headers["Location"]


def check_profile_redirection_get(app, client, url):
    # creating the app context
    with app.app_context():
        response = client.get(url)
        # converting to response object
        resp = make_response(response)
        # redirects to login page
        assert '/profile' in resp.headers["Location"]


def check_nonauth_menu_get(client, url):
    response = client.get(url)
    assert b'a href="/index"' in response.data
    assert b'a href="/login"' in response.data
    assert b'a href="/register"' in response.data


def check_auth_menu_get(client, url):
    response = client.get(url)
    assert b'a href="/index"' in response.data
    assert b'li class="username"' in response.data
    assert b'a href="/logout"' in response.data


def check_index_data_get(client, url):
    response = client.get(url)
    assert b'table class="review"' in response.data


def check_rest_data_get(client, url):
    response = client.get(url)
    assert b'html' in response.data
    assert b'ul class="mainmenu"' in response.data
    assert b'h1 class="restaurant"' in response.data
    assert b'table class="review"' in response.data
    assert b'div class="feed"' in response.data
    assert b'p class="contacts"' in response.data


def check_nonexist_rest_get(client, url):
    check_404_get(client, url)


def check_my_profile_auth_data_get(client, url):
    response = client.get(url)
    check_auth_menu_get(client, url)
    assert b'html' in response.data
    assert b'class="profile-table"' in response.data
    assert b'div class="main-ava"' in response.data
    assert b'div class="profile-load"' in response.data
    assert b'form action="/upload"' in response.data
    assert b'ul class="profile-info"' in response.data
    assert b'a href="/logout"' in response.data
    assert b'h2' in response.data


def check_foreign_profile_auth_data_get(client, url):
    response = client.get(url)
    check_auth_menu_get(client, url)
    assert b'html' in response.data
    assert b'class="profile-table"' in response.data
    assert b'div class="main-ava"' in response.data
    assert b'ul class="profile-info"' in response.data
    assert b'h2' in response.data


def check_registration_data_get(client, url):
    response = client.get(url)
    check_nonauth_menu_get(client, url)
    assert b'h1 class="login"' in response.data
    assert b'form method="post" class="form-contact' in response.data
    assert b'label for="username"' in response.data
    assert b'input name="username"' in response.data
    assert b'label for="email"' in response.data
    assert b'input type="email" ' in response.data
    assert b'label for="password"' in response.data
    assert b'input type="password"' in response.data
    assert b'label for="password2"' in response.data
    assert b'input type="password2"' in response.data
    assert b'input type="submit"' in response.data


def check_login_data_get(client, url):
    response = client.get(url)
    check_nonauth_menu_get(client, url)
    assert b'h1 class="login"' in response.data
    assert b'form method="post" class="form-contact' in response.data
    assert b'label for="username"' in response.data
    assert b'input name="username"' in response.data
    assert b'label for="password"' in response.data
    assert b'input type="password"' in response.data
    assert b'input type="submit"' in response.data
    assert b'input type="email"' not in response.data
    assert b'input type="password2"' not in response.data


def check_registration_data_post(app, client, url):
    response = client.post(url, data={'username': 'aaaa',
                                      'email': 'sakd@kfsf',
                                      'password': 'aaaa',
                                      'password2': 'aaaa'}
                           )
    assert response.headers["Location"] == "/login"

    with app.app_context():
        assert FDataBase(get_db()).get_user_by_name('aaaa')


def check_login_data_post(client, auth):
    # logs in with 'test_name' and 'test' data
    response = auth.login()
    assert "/profile" in response.headers["Location"]

    # !!!allows accessing context variables such as session after the response is returned. Normally,
    # accessing session outside of a request would raise an error.
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user is not None
        assert g.user['username'] == 'test_name'


def check_validate_register(client, url, username, email, password, password2, message):
    response = client.post(url, data={'username': username,
                                      'email': email,
                                      'password': password,
                                      'password2': password2}
                           )
    assert message in response.data


def check_validate_login(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def check_logout_data_get(auth, client, url):
    response = auth.logout()
    # redirects to '/index' only at the 1st logout -> the order of methods is important
    assert '/index' in response.headers["Location"]
    check_status_code_302_get(client, url)
    check_content_text_type_get(client, url)

    with client:
        client.get('/')
        assert g.user is None
        assert 'user_id' not in session


def check_leave_feedback_data_get(client, url):
    response = client.get(url)
    check_auth_menu_get(client, url)
    assert b'a class="leave"' in response.data
    assert b'form action="/leave_feedback' in response.data
    assert b'label for="title"' in response.data
    assert b'input id="title"' in response.data
    assert b'label for="body"' in response.data
    assert b'textarea id="body"' in response.data
    assert b'input type="submit"' in response.data


def check_feedback_data_get(client, url):
    response = client.get(url)
    check_auth_menu_get(client, url)
    assert b'img class="feedback"' in response.data
    assert b'p class="none"' in response.data
    assert b'a href="/restaurant' in response.data
    assert b'a href="/profile/' in response.data
    assert b'p class="annonce"' in response.data


def check_update_feedback_data_get(client, url):
    response = client.get(url)
    check_auth_menu_get(client, url)
    assert b'a class="leave" href="/feedback' in response.data
    assert b'a class="leave" href="/restaurant' in response.data
    assert b'form action="/update_feedback' in response.data
    assert b'label for="title"' in response.data
    assert b'input id="title"' in response.data
    assert b'label for="body"' in response.data
    assert b'textarea id="body"' in response.data
    assert b'input type="submit"' in response.data
    assert b'form action="/delete_feedback' in response.data
    assert b'input class="danger" type="submit"' in response.data
    assert b'onclick="return confirm' in response.data


def check_leave_feedback_data_post(client, url, app):
    response = client.post(url, data={'title': 'New feedback',
                                      'body': 'This is a new feedback'}
                           )
    assert '/all_feedbacks/restaurant' in response.headers["Location"]

    with app.app_context():
        # 1 feedback already exists in the database
        assert FDataBase(get_db()).get_feedback(2)

    # assert b'' in response.data
    # assert b'' in response.data


def check_update_feedback_data_post(app, client, url):
    response = client.post(url, data={'title': 'updated',
                                      'body': 'updated feedback'}
                           )
    assert '/update_feedback' in response.headers["Location"]

    with app.app_context():
        feedback = FDataBase(get_db()).get_feedback(1)
        assert feedback['title'] == 'updated'
        assert feedback['body'] == 'updated feedback'