import requests


def test_page_number():
    page = 2

    res = requests.get('https://reqres.in/api/users?page=2', params={'page': page})

    assert res.status_code == 200
    assert res.json()['per_page'] == 6


def test_user_list():
    default_user_count = 6
    res = requests.get('https://reqres.in/api/users?page=2')

    assert len(res.json()['data']) == default_user_count


def test_not_found():
    res = requests.get('https://reqres.in/api/users/23')

    assert res.status_code == 404
    assert res.text == '{}'


def test_create_user():
    name = "morpheus"
    res = requests.post('https://reqres.in/api/users', json={
        "name": name,
        "job": "leader"

    })

    assert res.status_code == 201
    assert res.json()['name'] == name


def test_delayed():
    res = requests.get('https://reqres.in/api/users?delay=3')

    assert res.status_code == 200
    assert res.json()['page'] == 1


def test_delete():
    res = requests.delete('https://reqres.in/api/users/2')

    assert res.status_code == 204
    assert res.text == ''


def test_update():
    res = requests.patch('https://reqres.in/api/users/2', json={
        "name": "morpheus",
        "job": "zion resident"
    })

    assert res.status_code == 200
    assert res.json()["job"] == 'zion resident'


def test_login_unsuccessful():
    res = requests.post('https://reqres.in/api/register', json={
        "email": "peter@klaven"
    })
    assert res.status_code == 400
    assert res.text == '{"error":"Missing password"}'


def test_single():
    res = requests.get('https://reqres.in/api/unknown/23')

    assert res.status_code == 404
    assert res.text == '{}'


def test_list_resource():
    res = requests.get('https://reqres.in/api/unknown')

    assert res.status_code == 200
    assert res.json()['total_pages'] == 2


def test_login_successful():
    res = requests.post('https://reqres.in/api/login', json={
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })

    assert res.status_code == 200
    assert res.text == '{"token":"QpwL5tke4Pnpja7X4"}'
