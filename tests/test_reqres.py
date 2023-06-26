import requests
from jsonschema.validators import validate

from helpers import load_json_schema


def test_page_number():
    schema = load_json_schema('sch_page_number.json')
    page = 2
    res = requests.get('https://reqres.in/api/users?page=2', params={'page': page})
    validate(instance=res.json(), schema=schema)
    assert res.status_code == 200
    assert res.json()['per_page'] == 6


def test_user_list():
    schema = load_json_schema('sch_user_list.json')
    default_user_count = 6
    res = requests.get('https://reqres.in/api/users?page=2')
    validate(instance=res.json(), schema=schema)
    assert len(res.json()['data']) == default_user_count


def test_not_found():
    schema = load_json_schema('sch_not_found.json')
    res = requests.get('https://reqres.in/api/users/23')
    validate(instance=res.json(), schema=schema)

    assert res.status_code == 404
    assert res.text == '{}'


def test_create_user():
    schema = load_json_schema('sch_create_user.json')
    name = "morpheus"
    res = requests.post('https://reqres.in/api/users', json={
        "name": name,
        "job": "leader"

    })
    validate(instance=res.json(), schema=schema)
    assert res.status_code == 201
    assert res.json()['name'] == name

def test_delayed():
    schema = load_json_schema('sch_delayed.json')
    res = requests.get('https://reqres.in/api/users?delay=3')
    validate(instance=res.json(), schema=schema)
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
    schema = load_json_schema('sch_update.json')
    validate(instance=res.json(), schema=schema)
    assert res.status_code == 200
    assert res.json()["job"] == 'zion resident'



def test_login_unsuccessful():
    res = requests.post('https://reqres.in/api/register', json={
        "email": "peter@klaven"
    })
    schema = load_json_schema('sch_loggin_un.json')
    validate(instance=res.json(), schema=schema)
    assert res.status_code == 400
    assert res.text == '{"error":"Missing password"}'


def test_single():
    res = requests.get('https://reqres.in/api/unknown/23')
    schema = load_json_schema('sch_single.json')
    validate(instance=res.json(), schema=schema)
    assert res.status_code == 404
    assert res.text == '{}'


def test_list_resource():
    res = requests.get('https://reqres.in/api/unknown')
    schema = load_json_schema('sch_list_resource.json')
    validate(instance=res.json(), schema=schema)

    assert res.status_code == 200
    assert res.json()['total_pages'] == 2


def test_login_successful():
    res = requests.post('https://reqres.in/api/login', json={
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    })
    schema = load_json_schema('sch_login_successful.json')
    validate(instance=res.json(), schema=schema)
    assert res.status_code == 200
    assert res.text == '{"token":"QpwL5tke4Pnpja7X4"}'
