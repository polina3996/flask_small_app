from flask import make_response

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
    assert b'form action="/register" method="post"' in response.data
    assert b'label for="username"' in response.data
    assert b'input id="username"' in response.data
    assert b'label for="email"' in response.data
    assert b'input id="email"' in response.data
    assert b'label for="psw"' in response.data
    assert b'input id="psw"' in response.data
    assert b'label for="psw2"' in response.data
    assert b'input id="psw2"' in response.data
    assert b'input id="submit"' in response.data


def check_registration_data_post(app, client, url):
    with app.test_request_context(url, method='POST'):
        #form = RegisterForm(username='aaaa', email='aaaa@gmail.com', psw='12345', psw2='12345')
        # POST-request, converting the *data-dictionary into form-data.
        # data contains the body of the response as bytes. If you expect a certain value to render on the page,
        # check that it’s in data. Bytes must be compared to bytes. If you want to compare text, use
        # get_data(as_text=True) instead.
        name = bytes('aaaa', 'utf-8')
        em = bytes('aaaa@gmail.com', 'utf-8')
        passw = bytes('12345', 'utf-8')
        # response = client.post(url, data={request.form["username"]: name,
        #                                   request.form["email"]: em,
        #                                   request.form["psw"]: passw,
        #                                   request.form["psw2"]: passw
        #                                   })
        # client.post(url, data={"username": "shdskhkh",
        #                        "email": "shddjs@gmail.com",
        #                        "psw":"12636",
        #                        "psw2":"12636"}
        #             )
        response = client.post(url, data={f'username': name,
                                          f'email': em,
                                          f'psw': passw,
                                          f'psw2': passw}, follow_redirects=True)
        # response = client.post(url)
        # response.get_data(as_text={f'{form.username.data}': 'aaaa',
        #                    f'{form.email.data}': 'aaaa@gmail.com',
        #                    f'{form.psw.data}': '12345',
        #                    f'{form.psw2.data}': '12345'
        #                    })
        # with app.app_context():
        #resp = make_response(response)
        assert response.headers["Location"] == '/login'
        assert FDataBase(get_db()).get_user_by_name(name)


# def check_validate_register(client, url, ):
#     response = client.post('/register', data={'username': username, 'password': password}
#         )
#         assert message in response.data

# assert b'' in response.data

