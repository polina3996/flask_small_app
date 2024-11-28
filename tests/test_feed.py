import pytest

from check_methods import check_status_code_200_get, check_content_text_type_get, check_auth_menu_get, \
    check_leave_feedback_data_get, check_leave_feedback_data_post, check_status_code_302_get, check_login_required_get, \
    check_404_get, check_feedback_data_get, check_update_feedback_data_get, check_update_feedback_data_post, \
    check_delete_feedback_data_post, check_all_feedbacks_data_get


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_leave_feedback(client, auth, rest_id, app):
    """Tests a handler where a logged in user 'test_name' may leave his feedback(it will be his second feedback, id=2);
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page where 'test_name' may leave his feedback on a restaurant (if restaurant exists),
     leaves the feedback and redirects to ALL FEEDBACKS OF A RESTAURANT"""
    # non logged in
    check_status_code_302_get(client, f'/leave_feedback/{rest_id}')
    check_content_text_type_get(client, f'/leave_feedback/{rest_id}')
    check_login_required_get(app, client, f'/leave_feedback/{rest_id}')

    # logged in
    auth.login()
    check_status_code_200_get(client, f'/leave_feedback/{rest_id}')
    check_404_get(client, f'/leave_feedback/100')
    check_content_text_type_get(client, f'/leave_feedback/{rest_id}')
    check_leave_feedback_data_get(client, f'/leave_feedback/{rest_id}')
    check_leave_feedback_data_post(client, f'/leave_feedback/{rest_id}', app)


def test_show_my_feedback(app, auth, client, feedback_id=1):
    """Tests a handler that shows a  feedback(id=1) of a logged in user 'test_name';
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page with a feedback with a possibility to EDIT it"""
    # non logged in
    check_status_code_302_get(client, f'/feedback/{feedback_id}')
    check_content_text_type_get(client, f'/feedback/{feedback_id}')
    check_login_required_get(app, client, f'/feedback/{feedback_id}')

    # logged in
    auth.login()
    check_status_code_200_get(client, f'/feedback/{feedback_id}')
    check_content_text_type_get(client, f'/feedback/{feedback_id}')
    check_feedback_data_get(client, f'/feedback/{feedback_id}')
    assert b'a class="new" href="/update_feedback' in client.get(f'/feedback/{feedback_id}').data


def test_show_foreign_feedback(app, auth, client, feedback_id=1):
    """Tests a handler that shows a feedback(id=1) of another user to a logged in user 'test_username';
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page with a feedback WITHOUT a possibility to edit it"""
    # non logged in
    check_status_code_302_get(client, f'/feedback/{feedback_id}')
    check_content_text_type_get(client, f'/feedback/{feedback_id}')
    check_login_required_get(app, client, f'/feedback/{feedback_id}')

    # logged in
    auth.login(username='test_username', password='test')
    check_status_code_200_get(client, f'/feedback/{feedback_id}')
    check_content_text_type_get(client, f'/feedback/{feedback_id}')
    check_feedback_data_get(client, f'/feedback/{feedback_id}')
    assert not b'a class="new" href="/update_feedback' in client.get(f'/feedback/{feedback_id}').data


def test_update_my_feedback(app, auth, client, feedback_id=1):
    """Tests a handler that updates a feedback(id=1) of a logged in user 'test_name';
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page where a user updates ot deletes his feedback; does it and stays at that very page"""
    # non logged in
    check_status_code_302_get(client, f'/update_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/update_feedback/{feedback_id}')
    check_login_required_get(app, client, f'/update_feedback/{feedback_id}')
    # logged in( with 'test_name' data!)
    auth.login()
    check_status_code_200_get(client, f'/update_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/update_feedback/{feedback_id}')
    check_update_feedback_data_get(client, f'/update_feedback/{feedback_id}')
    check_update_feedback_data_post(app, client, f'/update_feedback/{feedback_id}')


def test_update_foreign_feedback(app, auth, client, feedback_id=1):
    """Tests a handler that wants to update a feedback(id=1) of another user by a logged in user 'test_username';
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page 404 not found"""
    # non logged in
    check_status_code_302_get(client, f'/update_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/update_feedback/{feedback_id}')
    check_login_required_get(app, client, f'/update_feedback/{feedback_id}')
    # logged in( with 'test_username' data!)
    auth.login(username='test_username', password='test')
    check_status_code_200_get(client, f'/update_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/update_feedback/{feedback_id}')
    check_404_get(client, f'/update_feedback/{feedback_id}')


def test_delete_my_feedback(app, auth, client, feedback_id=1):
    """Tests a handler that deletes a feedback(id=1) of a logged in user 'test_name';
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page where a user updates ot deletes his feedback; does it and stays at that very page"""
    # non logged in
    check_status_code_302_get(client, f'/delete_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/delete_feedback/{feedback_id}')
    check_login_required_get(app, client, f'/delete_feedback/{feedback_id}')
    # logged in( with 'test_name' data!)
    auth.login()
    check_status_code_200_get(client, f'/delete_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/delete_feedback/{feedback_id}')
    check_update_feedback_data_get(client, f'/delete_feedback/{feedback_id}')
    check_delete_feedback_data_post(app, client, f'/delete_feedback/{feedback_id}')


def test_delete_foreign_feedback(app, auth, client, feedback_id=1):
    """Tests a handler that wants to delete a feedback(id=1) of another user by a logged in user 'test_username';
    the difference between logged in and non logged in are:
    - non logged in -> redirects to login;
    - logged in -> shows a page 404 not found"""
    # non logged in
    check_status_code_302_get(client, f'/update_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/update_feedback/{feedback_id}')
    check_login_required_get(app, client, f'/update_feedback/{feedback_id}')
    # logged in( with 'test_username' data!)
    auth.login(username='test_username', password='test')
    check_status_code_200_get(client, f'/update_feedback/{feedback_id}')
    check_content_text_type_get(client, f'/update_feedback/{feedback_id}')
    check_404_get(client, f'/update_feedback/{feedback_id}')


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_all_feedbacks(client, app, rest_id, auth):
    # non logged in
    check_status_code_302_get(client, f'/all_feedbacks/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/all_feedbacks/restaurant/{rest_id}')
    check_login_required_get(app, client, f'/all_feedbacks/restaurant/{rest_id}')

    # logged in
    auth.login()
    check_status_code_200_get(client, f'/all_feedbacks/restaurant/{rest_id}')
    check_content_text_type_get(client, f'/all_feedbacks/restaurant/{rest_id}')
    check_all_feedbacks_data_get(client, f'/all_feedbacks/restaurant/{rest_id}')

