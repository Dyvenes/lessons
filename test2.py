import pytest
import requests
from flask import jsonify

from data import db_session
from data.db_session import global_init, create_session
from data.users import User

base_url = 'http://127.0.0.1:5000'


@pytest.fixture
def db_init():
    global_init('db/mars_explorer.db')


def test_get_one_user(db_init):
    response = requests.get(base_url + '/api/v2/users/1')
    sess = create_session()
    user = sess.query(User).get(1)
    assert response.json() == {'user': user.to_dict(rules=('-jobs',))}


def test_get_wrong_user(db_init):
    user_id = 999
    response = requests.get(base_url + f'/api/v2/users/{user_id}')
    assert response.json() == {'message': f'User {user_id} not found'}


def test_get_all_user(db_init):
    response = requests.get(base_url + '/api/v2/users')
    session = db_session.create_session()
    users = session.query(User).all()
    assert response.json() == {'users':
                                   [item.to_dict(only=('id', 'name', 'surname', 'email', 'jobs.id', 'jobs.job'), )
                                    for item in users]}


def test_post_user(db_init):
    user_json = {
        'id': 4,
        'surname': 'Фамилия',
        'name': 'Имя',
        'age': 10,
        'position': 'позиция',
        'speciality': 'специяльность',
        'address': "адрес",
        'email': 'email121233@mail.ru',
    }
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {'success': 'OK'}


def test_post_user_wrong_param(db_init):
    user_json = {
        'id': 4,
        'surname': 'Фамилия',
        'name': 'Имя',
        'age': 'qwer',
        'position': 'позиция',
        'speciality': 'специяльность',
        'address': "адрес",
        'email': 'email123@mail.ru',
    }
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {'message': {'age': "invalid literal for int() with base 10: 'qwer'"}}


def test_post_user_empty_param(db_init):
    user_json = {}
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {
        'message': {'id': 'Missing required parameter in the JSON body or the post body or the query string'}}


def test_post_user_missed_param(db_init):
    user_json = {
        'name': 'Имя',
        'age': '10',
        'speciality': 'специяльность',
        'email': 'email123@mail.ru',
    }
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {
        'message': {'id': 'Missing required parameter in the JSON body or the post body or the query string'}}


def test_exist_user(db_init):
    user_json = {
        'id': 3,
        'surname': 'Фамилия',
        'name': 'Имя',
        'age': 10,
        'position': 'позиция',
        'speciality': 'специяльность',
        'address': "адрес",
        'email': 'email123@mail.ru',
    }
    response = requests.post(base_url + '/api/v2/users', json=user_json)
    assert response.json() == {'error': 'Id already exist'}


def test_delete_user(db_init):
    response = requests.delete(base_url + '/api/v2/users/4')
    assert response.json() == {'success': 'ok'}
