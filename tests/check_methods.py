from flask import make_response


def check_status_code_200_get(client, url):
    response = client.get(url)
    assert response.status_code == 200


def check_status_code_302_get(client, url):
    response = client.get(url)
    assert response.status_code == 302


def check_content_text_type_get(client, url):
    response = client.get(url)
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


def check_index_data_get(client, url='/index'):
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


def check_profile_auth_data_get(client, url):
    response = client.get(url)
    check_auth_menu_get(client, url)
    assert b'html' in response.data
    assert b'table class="profile-table"' in response.data
    assert b'div class ="profile-ava"' in response.data
    assert b'div class="profile-load"' in response.data
    assert b'form action="/upload"' in response.data
    assert b'ul class="profile-info"' in response.data
    assert b'a href="/logout"' in response.data
    assert b'h2' in response.data

    # assert b'' in response.data
