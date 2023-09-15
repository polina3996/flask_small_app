def check_status_code(client, url):
    response = client.get(url)
    assert response.status_code == 200


def check_content_type(client, url):
    response = client.get(url)
    assert response.content_type == 'text/html; charset=utf-8'


def check_nonauth_menu(client, url):
    response = client.get(url)
    assert b'a href="/index"' in response.data
    assert b'a href="/login"' in response.data
    assert b'a href="/register"' in response.data


def check_auth_menu(client, url):
    response = client.get(url)
    assert b'a href="/index"' in response.data
    assert b'li class="username"' in response.data
    assert b'a href="/logout"' in response.data


def check_index_data(client, url='/index'):
    response = client.get(url)
    assert b'table class="review"' in response.data


def check_rest_data(client, url):
    response = client.get(url)
    assert b'html' in response.data
    assert b'ul class="mainmenu"' in response.data
    assert b'h1 class="restaurant"' in response.data
    assert b'table class="review"' in response.data
    assert b'div class="feed"' in response.data
    assert b'p class="contacts"' in response.data


def check_nonexist_rest(client, url):
    response = client.get(url)
    assert b'html' in response.data
    assert b'p class="none"' in response.data