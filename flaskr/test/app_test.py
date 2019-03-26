import os
import tempfile

import pytest

import app as flaskr


@pytest.fixture
def client():
    flaskr.app.config['TESTING'] = True
    client = flaskr.app.test_client()

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


def test_mentee(client):

    rv = client.get('/mentee')
    assert 404 == rv.status_code

def test_mentor(client):

    rv = client.get('/mentor')
    assert 404 == rv.status_code

def test_arguments(client):
    with flaskr.app.test_request_context('/?id=123'):
        assert flaskr.request.path == '/'
        assert flaskr.request.args['id'] == '123'