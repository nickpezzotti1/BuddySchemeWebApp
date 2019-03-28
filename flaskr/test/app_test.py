import os
import tempfile

import pytest

import flaskr
import flask

app = flaskr.create_app()

@pytest.fixture
def client():

    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_ping(client):

    rv = client.get('/ping')
    assert b'pong' in rv.data

def test_login(client):

    rv = client.get('/login')
    assert 200 == rv.status_code

def test_admin(client):

    rv = client.get('/admin')
    assert 302 == rv.status_code


def test_user(client):

    rv = client.get('/user')
    assert 302 == rv.status_code

def test_arguments(client):
    with app.test_request_context('/?id=123'):
        assert flask.request.path == '/'
        assert flask.request.args['id'] == '123'
